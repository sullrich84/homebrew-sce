import sys
import argparse
from sce.extract import SlackExtractor
from sce.transform import VCardTransformer
from sce.globals import (
    app_version,
    app_name,
    app_full_name,
    app_description,
    app_epilog,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=app_name,
        description=app_description,
        epilog=app_epilog,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="print sce version",
        action="version",
        version=f"%(prog)s {app_version}",
    )

    parser.add_argument(
        "-t",
        "--token",
        metavar="xoxp-1234",
        required=True,
        help="set slack service token (required scopes: user:read, user:read.email)",
        type=str,
    )

    parser.add_argument(
        "-g",
        "--organization",
        metavar='"Slack Inc."',
        required=True,
        help="set organization of contacts",
        type=str,
    )

    parser.add_argument(
        "-r",
        "--implied_phone_region",
        metavar="DE",
        required=True,
        help="set alpha-2 country code used to imply incomplete phone numbers",
        type=str,
    )

    parser.add_argument(
        "-s",
        "--implied_email_schema",
        metavar="\$given_name.\$family_name@slack.com",
        help="set email schema that will be used to imply unknown email addresses.",
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="export",
        help="set output folder",
        type=str,
        default="contacts",
    )

    parser.add_argument(
        "-l",
        "--limit",
        metavar="25",
        help="set export limit of contacts",
        type=int,
        default=0,
    )

    return parser.parse_args()


def cli():
    try:
        args = parse_arguments()

        print(f"{app_full_name} v{app_version}")
        print()

        extractor = SlackExtractor(
            token=args.token,
        )

        transformer = VCardTransformer(
            implied_phone_region=args.implied_phone_region,
            organization=args.organization,
            email_schema=args.implied_email_schema,
        )

        extracted_vcards = extractor.extract()
        if args.limit > 0:
            extracted_vcards = extracted_vcards[: args.limit]

        transformed_vcards = transformer.transform(extracted_vcards)

        for transformed_vcard in transformed_vcards:
            outfile = f"{args.output}/{transformed_vcard.uid}.vcf"
            with open(outfile, "w", encoding="utf-8") as output:
                vcard_str = transformed_vcard.render()
                output.write(vcard_str)

        print(f"{len(transformed_vcards)} contacts written to {args.output}")

    except KeyboardInterrupt:
        print("Aborted by user.")
        sys.exit(0)


if __name__ == "__main__":
    cli()
