# Chromedriver - AutoInstall

A very simple Python script to just get the latest Chromedriver version from their endpoint, download and extract it to the folder you want.

## Usage

Either you can use the .pyz in the releases directly, by just running `python chromedriver_downloader.pyz <PATH TO OUTPUT .EXE>`

To build the pyz on your own, you can do the following:
1. Clone the repository
2. In the repository folder run: `python -m pip install -r requirements.txt --target modules/`
3. Then move out of the repository folder, and run the command: `python -m zipapp <REPO_NAME>/ -o chromedriver_downloader.pyz -c`

