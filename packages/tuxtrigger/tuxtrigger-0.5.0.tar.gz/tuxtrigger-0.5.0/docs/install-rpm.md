
## Installing the RPM packages 


!!! note
    TuxTrigger requires Python 3.6 or newer.


To install TuxTrigger on your system globally:

1. Create /etc/yum.repos.d/tuxtrigger.repo with the following contents:

```shell
[tuxtrigger]
name=tuxtrigger
type=rpm-md
baseurl=https://linaro.gitlab.io/tuxtrigger/packages/
gpgcheck=1
gpgkey=https://linaro.gitlab.io/tuxtrigger/packages/repodata/repomd.xml.key
enabled=1
```

2. Install tuxtrigger as you would any other package:

```shell
# dnf install tuxtrigger
```

Upgrades will be available in the same repository, so you can get them using the same procedure you already use to get other updates for your system.

