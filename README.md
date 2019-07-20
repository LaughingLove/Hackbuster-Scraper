# Hackbuster Scraper to E-Mail
### Checks hackbuster every 30 minutes for the newest article, and sends it to you via email

## Setup

Clone the repo then:

Create a `personal_config.json` file and set it up like this:

```json
{
    "email": "youremail@email.com",
    "password": "your smtp password here"
}
```

To create an SMTP password for services like GMail, you're going to need to create an app password, which is located *[here](https://myaccount.google.com/apppasswords)*.

You will need to download a web driver in order for selenium to run properly.

Downloads for the webdrivers:

- [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [Firefox](https://github.com/mozilla/geckodriver/releases/tag/v0.24.0)
- [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads)

Any other browsers just search `{browser} web driver` and you should find it. When you download the web driver you need to add it to your path, and the equivilent is on linux.

After you do this, then just do this command:

`py main.py`

