#!/usr/bin/env python3
from random import shuffle
from collections import defaultdict
import argparse
import sys

import requests


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--participant",
        required=True,
        nargs=3,
        action='append',
        help="group, name, and email (e.g. '1 John john@domain.com')")
    parser.add_argument(
        "--mailgun-key",
        required=True,
        help="Mailgun API key")
    parser.add_argument(
        "--mailgun-domain",
        required=True,
        help="Mailgun domain, e.g. mailgun.domain.com")
    parser.add_argument("--email-sender", default="santa")
    parser.add_argument("--email-subject", default="Secret Santa")
    parser.add_argument("--email-body", default="You drew {name}!")
    
    args = parser.parse_args(sys.argv[1:])

    groups = parse_groups(args)

    picks = draw(groups)
    
    for (giver_name, giver_email), (taker, _) in picks:
        send_email(args, giver_email, taker)


def parse_groups(args: argparse.Namespace):

    groups = defaultdict(list)
    for (group, name, email) in args.participant:
        groups[group].append((name, email))

    return list(groups.values())


def draw(groups: dict) -> list:

    participants1 = [person for group in groups for person in group]
    participants2 = [person for person in participants1]

    groups = {
        participant: group_index
        for group_index, members in enumerate(groups)
        for participant in members
    }

    valid = False

    # Shuffle until nobody picks anyone from their own group:
    while not valid:
        shuffle(participants2)
        pairs = list(zip(participants1, participants2))

        valid = all(groups[p1] != groups[p2] for (p1, p2) in pairs)

    return pairs


def send_email(args: argparse.Namespace, address: str, name: str) ->  None:

    request_url = f"https://api.mailgun.net/v2/{args.mailgun_domain}/messages"
    from_address = f"{args.email_sender}@{args.mailgun_domain}"
    body = args.email_body.format(name=name)
    
    print("Sending email to %s" % address)
    
    response = requests.post(
        request_url,
        auth=('api', args.mailgun_key), data={
            'from': from_address,
            'to': address,
            'subject': args.email_subject,
            'text': body,
        },
        verify=True,
    )

     
if __name__ == '__main__':
    main()
