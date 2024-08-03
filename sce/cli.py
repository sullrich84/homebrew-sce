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
        help="prints the applications version",
        action="version",
        version=f"%(prog)s {app_version}",
    )

    parser.add_argument(
        "--token",
        required=True,
        help="slack service token",
        type=str,
    )

    parser.add_argument(
        "--organization",
        required=True,
        help="name of organization",
        type=str,
    )

    parser.add_argument(
        "--implied_phone_region",
        required=True,
        help="country code that will be implied to complete phone numbers",
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        type=str,
        default="contacts.vcf",
    )

    parser.add_argument(
        "-l",
        "--limit",
        help="limits the total amout of users",
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
        )

        extracted_vcards = extractor.extract()
        if args.limit > 0:
            extracted_vcards = extracted_vcards[:args.limit]

        transformed_vcards = transformer.transform(extracted_vcards)

        with open(args.output, "w", encoding="utf-8") as output:
            for transformed_vcard in transformed_vcards:
                vcard_str = transformed_vcard.render()
                output.write(vcard_str)

        print(f"{len(transformed_vcards)} contacts written to {args.output}")

    except KeyboardInterrupt:
        print("Aborted by user.")
        sys.exit(0)


if __name__ == "__main__":
    cli()
