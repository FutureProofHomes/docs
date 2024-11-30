#!/usr/bin/env python3

import sys
import os
import json
import hashlib
import urllib.request
import urllib.error

# Set the path to the directory containing this script and add it to the system path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from utils import utils


def process_build(
    BASE_NAME,
    build_assets_info,
    release_tag,
    beta,
    release_repository,
    GITHUB_TOKEN,
):
    # Get the Asset ID for the OTA binaries
    # Sample URL: https://api.github.com/repos/FutureProofHomes/Satellite1-ESPHome/releases/assets/210089213
    BASE_URL=f"https://api.github.com/repos/{release_repository}/releases/assets/"    
    BROWSER_URL_FACTORY = build_assets_info.get('factory', {}).get('browser_download_url')
    BROWSER_URL_OTA = build_assets_info.get('ota', {}).get('browser_download_url')

    OTA_ASSET_ID = build_assets_info.get('ota', {}).get('asset_id')
    DOWNLOAD_URL = f"{BASE_URL}{OTA_ASSET_ID}"
    print(f"Factory URL: {BROWSER_URL_FACTORY}")
    print(f"OTA URL: {BROWSER_URL_OTA}")
    # Compute OTA_MD5 if BROWSER_URL_OTA is available
    OTA_MD5 = ""
    # Compute OTA_MD5 if BROWSER_URL_OTA is available
    if BROWSER_URL_OTA:
        headers = {
            "Accept": "application/octet-stream",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        request = urllib.request.Request(DOWNLOAD_URL, headers=headers)
        try:
            with urllib.request.urlopen(request) as response:
                ota_data = response.read()
            OTA_MD5 = hashlib.md5(ota_data).hexdigest()
        except urllib.error.HTTPError as e:
            utils.error_exit(f"Failed to download OTA binary for {BASE_NAME}: {e}")

    # Check if the firmware directory exists
    MANIFEST_FILE_DIR = os.path.join("..", "assets", "manifests", BASE_NAME, release_tag)

    # Call the make_manifest function
    utils.make_manifest(
        BASE_NAME,
        release_tag,
        release_repository,
        BROWSER_URL_OTA,
        OTA_MD5,
        BROWSER_URL_FACTORY,
        MANIFEST_FILE_DIR,
        beta,
    )


def main():
    # Check if at least two parameters are passed
    # if len(sys.argv) < 3:
    #     utils.error_exit(f"Usage: {sys.argv[0]} <release_tag> <release_repository>")

    # Assign input parameters to variables
    # release_tag = sys.argv[1]
    # release_repository = sys.argv[2]
    
    release_tag = "v2.0.0-alpha.54"
    release_repository = "FutureProofHomes/Satellite1-ESPHome"
    # Ensure GITHUB_TOKEN is set
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        utils.error_exit("GITHUB_TOKEN is not set.")
    print(f"Fetching release info for {release_tag} from {release_repository}")
    # Determine if the release is a beta release.
    beta = any(keyword in release_tag.lower() for keyword in ["beta", "alpha", "rc"])

    data = utils.get_release_info(release_tag, release_repository, GITHUB_TOKEN)

    if not data:
        utils.error_exit(f"Failed to fetch release info for {release_tag}")

    # Parse the JSON data
    release_info = json.loads(data.decode("utf-8"))

    assets = release_info.get("assets", [])

    # Declare dictionaries to hold the URLs
    factory_urls = {}
    ota_urls = {}

    # Process the assets to build the dictionaries
    for asset in assets:
        print(f"Processing asset: {asset.get('name')}")
        name = asset.get("name")
        asset_id = asset.get("id") # Get the Asset ID
        # url = asset.get("browser_download_url")

        assets_info = {}

        for asset in assets:
            print(f"Processing asset: {asset.get('name')}")
            name = asset.get("name")
            asset_id = asset.get("id")
            browser_download_url = asset.get("browser_download_url")

            if name.endswith(".factory.bin"):
                build_name = name[: -len(".factory.bin")]
                if build_name not in assets_info:
                    assets_info[build_name] = {}
                assets_info[build_name]['factory'] = {
                    'browser_download_url': browser_download_url,
                    'asset_id': asset_id
                }
            elif name.endswith(".ota.bin"):
                build_name = name[: -len(".ota.bin")]
                if build_name not in assets_info:
                    assets_info[build_name] = {}
                assets_info[build_name]['ota'] = {
                    'browser_download_url': browser_download_url,
                    'asset_id': asset_id
                }

    # Process each build
    for BASE_NAME, build_assets_info in assets_info.items():
        process_build(
            BASE_NAME,
            build_assets_info,
            release_tag,
            beta,
            release_repository,
            GITHUB_TOKEN,
        )


if __name__ == "__main__":
    main()
