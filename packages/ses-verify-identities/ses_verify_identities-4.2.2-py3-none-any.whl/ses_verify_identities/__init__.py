'''
# @seeebiii/ses-verify-identities

This package provides two constructs helping you to verify identities in [AWS SES](https://aws.amazon.com/ses/) using the [AWS CDK](https://aws.amazon.com/cdk/).

For more information about verifying identities in AWS SES, [read the documentation](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html).

## Install

### npm

```shell
npm i -D @seeebiii/ses-verify-identities
```

See more details on npmjs.com: https://www.npmjs.com/package/@seeebiii/ses-verify-identities

### Maven

```xml
<dependency>
  <groupId>de.sebastianhesse.cdk-constructs</groupId>
  <artifactId>ses-verify-identities</artifactId>
  <version>4.0.2</version>
</dependency>
```

See more details on mvnrepository.com: https://mvnrepository.com/artifact/de.sebastianhesse.cdk-constructs/ses-verify-identities/

### Python

```shell
pip install ses-verify-identities
```

See more details on PyPi: https://pypi.org/project/ses-verify-identities/

### Dotnet / C#

You can find the details here: https://www.nuget.org/packages/Ses.Verify.Identities/

## Usage

Examples below are based on TypeScript.
See [API.md](API.md) for a full reference.

### Verify a Domain

```python
new VerifySesDomain(this, 'SesDomainVerification', {
  domainName: 'example.org'
});
```

#### Options

* `domainName` A domain name to be used for the SES domain identity, e.g. 'example.org'
* `hostedZoneName` A hosted zone name to be matched with a Route 53 record, e.g. 'example.org'. Default: same as `domainName`.
* `addTxtRecord` Whether to automatically add a TXT record to the hosed zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `addMxRecord` Whether to automatically add a MX record to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `addDkimRecord` Whether to automatically add DKIM records to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: `true`.
* `notificationTopic` An SNS topic where bounces, complaints or delivery notifications can be sent to. If none is provided, a new topic will be created and used for provided notification types.
* `notificationTypes` Select for which notification types you want to configure a topic. Default: `[Bounce, Complaint]`.
* `removalPolicy` Set a `RemovalPolicy` if you want to retain the resources. Default: `DESTROY`

### Verify an Email Address

```python
new VerifySesEmailAddress(this, 'SesEmailVerification', {
  emailAddress: 'hello@example.org'
});
```

#### Options

* `emailAddress` The email address to be verified, e.g. `hello@example.org`.
* `region` An optional AWS region to validate the email address. Default: The custom resource will be created in the stack region.
* `removalPolicy` Set a `RemovalPolicy` if you want to retain the resources. Default: `DESTROY`

## Contributing

I'm happy to receive any contributions!
Just open an issue or pull request :)

These commands should help you while developing:

* `npx projen`      init [projen](https://github.com/projen/projen) and synthesize changes in [.projenrc.js](.projenrc.js) to the project
* `yarn build`      compile typescript to js
* `yarn watch`      watch for changes and compile
* `yarn test`       perform the jest unit tests
* `yarn eslint`     validate code against best practices

## Author

[Sebastian Hesse](https://www.sebastianhesse.de) - Freelancer for serverless cloud projects on AWS.

## License

MIT License

Copyright (c) 2022 [Sebastian Hesse](https://www.sebastianhesse.de)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_sns
import constructs


@jsii.data_type(
    jsii_type="@seeebiii/ses-verify-identities.IVerifySesDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "add_dkim_records": "addDkimRecords",
        "add_mx_record": "addMxRecord",
        "add_txt_record": "addTxtRecord",
        "hosted_zone_id": "hostedZoneId",
        "hosted_zone_name": "hostedZoneName",
        "notification_topic": "notificationTopic",
        "notification_types": "notificationTypes",
        "removal_policy": "removalPolicy",
    },
)
class IVerifySesDomainProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        add_dkim_records: typing.Optional[builtins.bool] = None,
        add_mx_record: typing.Optional[builtins.bool] = None,
        add_txt_record: typing.Optional[builtins.bool] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        hosted_zone_name: typing.Optional[builtins.str] = None,
        notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
        notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''
        :param domain_name: A domain name to be used for the SES domain identity, e.g. 'sub-domain.example.org'.
        :param add_dkim_records: Whether to automatically add DKIM records to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param add_mx_record: Whether to automatically add a MX record to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param add_txt_record: Whether to automatically add a TXT record to the hosed zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param hosted_zone_id: Optional: A hosted zone id to be used for retrieving the Route53 hosted zone for adding new records. Providing an id will skip the hosted zone lookup.
        :param hosted_zone_name: A hosted zone name to be used for retrieving the Route53 hosted zone for adding new record, e.g. 'example.org'. If you also provide hostedZoneId, it is assumed that these values are correct and no lookup happens. Default: same as domainName
        :param notification_topic: An SNS topic where bounces, complaints or delivery notifications can be sent to. If none is provided, a new topic will be created and used for all different notification types. Default: new topic will be created
        :param notification_types: Select for which notification types you want to configure a topic. Default: [Bounce, Complaint]
        :param removal_policy: Whether to DESTROY or RETAIN the domain on removal. Default: DESTROY
        '''
        if __debug__:
            def stub(
                *,
                domain_name: builtins.str,
                add_dkim_records: typing.Optional[builtins.bool] = None,
                add_mx_record: typing.Optional[builtins.bool] = None,
                add_txt_record: typing.Optional[builtins.bool] = None,
                hosted_zone_id: typing.Optional[builtins.str] = None,
                hosted_zone_name: typing.Optional[builtins.str] = None,
                notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
                notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
                removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument add_dkim_records", value=add_dkim_records, expected_type=type_hints["add_dkim_records"])
            check_type(argname="argument add_mx_record", value=add_mx_record, expected_type=type_hints["add_mx_record"])
            check_type(argname="argument add_txt_record", value=add_txt_record, expected_type=type_hints["add_txt_record"])
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
            check_type(argname="argument notification_topic", value=notification_topic, expected_type=type_hints["notification_topic"])
            check_type(argname="argument notification_types", value=notification_types, expected_type=type_hints["notification_types"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if add_dkim_records is not None:
            self._values["add_dkim_records"] = add_dkim_records
        if add_mx_record is not None:
            self._values["add_mx_record"] = add_mx_record
        if add_txt_record is not None:
            self._values["add_txt_record"] = add_txt_record
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if hosted_zone_name is not None:
            self._values["hosted_zone_name"] = hosted_zone_name
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic
        if notification_types is not None:
            self._values["notification_types"] = notification_types
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''A domain name to be used for the SES domain identity, e.g. 'sub-domain.example.org'.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def add_dkim_records(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically add DKIM records to the hosted zone of your domain.

        This only works if your domain is
        managed by Route53. Otherwise disable it.

        :default: true
        '''
        result = self._values.get("add_dkim_records")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def add_mx_record(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically add a MX record to the hosted zone of your domain.

        This only works if your domain is
        managed by Route53. Otherwise disable it.

        :default: true
        '''
        result = self._values.get("add_mx_record")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def add_txt_record(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically add a TXT record to the hosed zone of your domain.

        This only works if your domain is
        managed by Route53. Otherwise disable it.

        :default: true
        '''
        result = self._values.get("add_txt_record")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''Optional: A hosted zone id to be used for retrieving the Route53 hosted zone for adding new records.

        Providing an
        id will skip the hosted zone lookup.
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone_name(self) -> typing.Optional[builtins.str]:
        '''A hosted zone name to be used for retrieving the Route53 hosted zone for adding new record, e.g. 'example.org'. If you also provide hostedZoneId, it is assumed that these values are correct and no lookup happens.

        :default: same as domainName
        '''
        result = self._values.get("hosted_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        '''An SNS topic where bounces, complaints or delivery notifications can be sent to.

        If none is provided, a new topic
        will be created and used for all different notification types.

        :default: new topic will be created
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.ITopic], result)

    @builtins.property
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Select for which notification types you want to configure a topic.

        :default: [Bounce, Complaint]
        '''
        result = self._values.get("notification_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''Whether to DESTROY or RETAIN the domain on removal.

        :default: DESTROY
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IVerifySesDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@seeebiii/ses-verify-identities.IVerifySesEmailAddressProps",
    jsii_struct_bases=[],
    name_mapping={
        "email_address": "emailAddress",
        "region": "region",
        "removal_policy": "removalPolicy",
    },
)
class IVerifySesEmailAddressProps:
    def __init__(
        self,
        *,
        email_address: builtins.str,
        region: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''
        :param email_address: The email address to be verified, e.g. 'hello@example.org'.
        :param region: An optional AWS region to validate the email address. Default: The custom resource will be created in the stack region
        :param removal_policy: Whether to DESTROY or RETAIN the email address on removal. Default: DESTROY
        '''
        if __debug__:
            def stub(
                *,
                email_address: builtins.str,
                region: typing.Optional[builtins.str] = None,
                removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[str, typing.Any] = {
            "email_address": email_address,
        }
        if region is not None:
            self._values["region"] = region
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def email_address(self) -> builtins.str:
        '''The email address to be verified, e.g. 'hello@example.org'.'''
        result = self._values.get("email_address")
        assert result is not None, "Required property 'email_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''An optional AWS region to validate the email address.

        :default: The custom resource will be created in the stack region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''Whether to DESTROY or RETAIN the email address on removal.

        :default: DESTROY
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IVerifySesEmailAddressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VerifySesDomain(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-verify-identities.VerifySesDomain",
):
    '''A construct to verify a SES domain identity.

    It initiates a domain verification and can automatically create
    appropriate records in Route53 to verify the domain. Also, it's possible to attach a notification topic for bounces,
    complaints or delivery notifications.

    Example::

        new VerifySesDomain(this, 'SesDomainVerification', {
          domainName: 'example.org'
        });
    '''

    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        domain_name: builtins.str,
        add_dkim_records: typing.Optional[builtins.bool] = None,
        add_mx_record: typing.Optional[builtins.bool] = None,
        add_txt_record: typing.Optional[builtins.bool] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        hosted_zone_name: typing.Optional[builtins.str] = None,
        notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
        notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param domain_name: A domain name to be used for the SES domain identity, e.g. 'sub-domain.example.org'.
        :param add_dkim_records: Whether to automatically add DKIM records to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param add_mx_record: Whether to automatically add a MX record to the hosted zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param add_txt_record: Whether to automatically add a TXT record to the hosed zone of your domain. This only works if your domain is managed by Route53. Otherwise disable it. Default: true
        :param hosted_zone_id: Optional: A hosted zone id to be used for retrieving the Route53 hosted zone for adding new records. Providing an id will skip the hosted zone lookup.
        :param hosted_zone_name: A hosted zone name to be used for retrieving the Route53 hosted zone for adding new record, e.g. 'example.org'. If you also provide hostedZoneId, it is assumed that these values are correct and no lookup happens. Default: same as domainName
        :param notification_topic: An SNS topic where bounces, complaints or delivery notifications can be sent to. If none is provided, a new topic will be created and used for all different notification types. Default: new topic will be created
        :param notification_types: Select for which notification types you want to configure a topic. Default: [Bounce, Complaint]
        :param removal_policy: Whether to DESTROY or RETAIN the domain on removal. Default: DESTROY
        '''
        if __debug__:
            def stub(
                parent: constructs.Construct,
                name: builtins.str,
                *,
                domain_name: builtins.str,
                add_dkim_records: typing.Optional[builtins.bool] = None,
                add_mx_record: typing.Optional[builtins.bool] = None,
                add_txt_record: typing.Optional[builtins.bool] = None,
                hosted_zone_id: typing.Optional[builtins.str] = None,
                hosted_zone_name: typing.Optional[builtins.str] = None,
                notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
                notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
                removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IVerifySesDomainProps(
            domain_name=domain_name,
            add_dkim_records=add_dkim_records,
            add_mx_record=add_mx_record,
            add_txt_record=add_txt_record,
            hosted_zone_id=hosted_zone_id,
            hosted_zone_name=hosted_zone_name,
            notification_topic=notification_topic,
            notification_types=notification_types,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @builtins.property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> aws_cdk.aws_sns.ITopic:
        '''The SNS topic where bounces, complaints or delivery notifications can be sent to.'''
        return typing.cast(aws_cdk.aws_sns.ITopic, jsii.get(self, "notificationTopic"))


class VerifySesEmailAddress(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-verify-identities.VerifySesEmailAddress",
):
    '''A construct to verify an SES email address identity.

    It initiates a verification so that SES sends a verification email to the desired email address. This means the owner of the email address still needs to act by clicking the link in the verification email.

    Example::

        .org'
        });
    '''

    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        email_address: builtins.str,
        region: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param email_address: The email address to be verified, e.g. 'hello@example.org'.
        :param region: An optional AWS region to validate the email address. Default: The custom resource will be created in the stack region
        :param removal_policy: Whether to DESTROY or RETAIN the email address on removal. Default: DESTROY
        '''
        if __debug__:
            def stub(
                parent: constructs.Construct,
                name: builtins.str,
                *,
                email_address: builtins.str,
                region: typing.Optional[builtins.str] = None,
                removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IVerifySesEmailAddressProps(
            email_address=email_address, region=region, removal_policy=removal_policy
        )

        jsii.create(self.__class__, self, [parent, name, props])


__all__ = [
    "IVerifySesDomainProps",
    "IVerifySesEmailAddressProps",
    "VerifySesDomain",
    "VerifySesEmailAddress",
]

publication.publish()
