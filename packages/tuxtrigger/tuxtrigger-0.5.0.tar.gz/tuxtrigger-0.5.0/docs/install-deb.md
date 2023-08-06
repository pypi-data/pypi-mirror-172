
## Installing the Debian packages


!!! note
    TuxTrigger requires Python 3.6 or newer.


1. Download the repository signing key to /etc/apt/trusted.gpg.d/:

```shell
# wget -O /etc/apt/trusted.gpg.d/tuxtrigger.gpg https://linaro.gitlab.io/tuxtrigger/packages/signing-key.gpg
```
2. Create /etc/apt/sources.list.d/tuxtrigger.list with the following contents:
```shell
deb https://linaro.gitlab.io/tuxtrigger/packages/ ./
```

3. Install tuxtrigger as you would any other package:

```shell
# apt update
# apt install tuxtrigger
```

Upgrading tuxtrigger will work just like it would for any other package (apt update, apt upgrade).
