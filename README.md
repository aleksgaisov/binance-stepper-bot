# Binance Stepper Bot

The 'binance-stepper-bot' ...

### Setting up

##### Bot-side

1. Make sure you have Python >= 3.7 installed
2. Download all the repository files to your machine or clone it:

```
git clone https://github.com/aleksgaisov/binance-stepper-bot
```
3. Install all the necessary dependencies listed in _requirements.txt_:

```
pip3 install -r requirements.txt
```

List:

```
python-binance
requests
autobahn
certifi
chardet
cryptography
dateparser
pyOpenSSL
service-identity
Twisted
```

##### Exchange-side

1. [Register/Log-in](https://accounts.binance.com/en/login) to Binance Exchange
2. Apply all the necessary security measures to protect your account, including Two-Factor Authentication.
3. Go to [API Manager](https://www.binance.com/en/usercenter/settings/api-management) and create new API with the following restrictions:

```
[*] Read Only    [*] Enable Trading    [] Enable Withdrawals

Optional: Consider restricting API access to trusted IPs only
```

4. Save your API and Secret keys

##### Email-side

As this bot uses Gmail as SMTP provider, follow the steps to allow it to send you reports.

1. [Allow less secure apps](https://www.google.com/settings/security/lesssecureapps) to access your account
2. [Display unlock captcha](https://accounts.google.com/DisplayUnlockCaptcha) to prevent _SMTPAuthenticationError_ with code 534

### Configuration

### Usage

### Trading Algorithm

### Disclaimer
