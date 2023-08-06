'''
[![npm version](https://badge.fury.io/js/enterprise-secure-bucket.svg)](https://badge.fury.io/js/enterprise-secure-bucket)
[![release](https://github.com/yvthepief/secure_bucket_construct/actions/workflows/release.yml/badge.svg)](https://github.com/yvthepief/secure_bucket_construct/actions/workflows/release.yml)

# Secure Bucket Construcs

Blog: https://yvovanzee.nl/secure-s3-bucket-construct-with-cdk-version-2

This Secure Bucket construcs extends the S3 Bucket construct. When using this construct, you will create a S3 bucket with default security best practises enabled. These are:

* Block public access
* Enabled versioning
* Enable enforce SSL to connect to bucket
* Enabled Bucket access logging
* Encryption of the bucket with a customer managed KMS key with enabled key rotation and trusted account identities.

These best practises are enforced. When creating a SecureBucket with for example versioning disabled, it will be overwritten to enabled.

# Usage

## install package

```bash
npm install @enterprise_secure_bucket
```

## Import the secure bucket construct in your code.

```python
// Import necessary packages
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { SecureBucket } from 'enterprise-secure-bucket';

export class SecureBucketStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new SecureBucket(this, 'myEnterpriseLevelSecureBucket',{});
  }
}
```
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
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import constructs


class SecureBucket(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="secure_bucket_construct.SecureBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        access_control: typing.Optional[aws_cdk.aws_s3.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[aws_cdk.aws_s3.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.CorsRule, typing.Dict[str, typing.Any]]]] = None,
        encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.IntelligentTieringConfiguration, typing.Dict[str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.Inventory, typing.Dict[str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.LifecycleRule, typing.Dict[str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.BucketMetrics, typing.Dict[str, typing.Any]]]] = None,
        notifications_handler_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        object_ownership: typing.Optional[aws_cdk.aws_s3.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[aws_cdk.aws_s3.RedirectTarget, typing.Dict[str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.RoutingRule, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Only relevant, when Encryption is set to {@link BucketEncryption.KMS} Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                access_control: typing.Optional[aws_cdk.aws_s3.BucketAccessControl] = None,
                auto_delete_objects: typing.Optional[builtins.bool] = None,
                block_public_access: typing.Optional[aws_cdk.aws_s3.BlockPublicAccess] = None,
                bucket_key_enabled: typing.Optional[builtins.bool] = None,
                bucket_name: typing.Optional[builtins.str] = None,
                cors: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.CorsRule, typing.Dict[str, typing.Any]]]] = None,
                encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
                encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
                enforce_ssl: typing.Optional[builtins.bool] = None,
                event_bridge_enabled: typing.Optional[builtins.bool] = None,
                intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.IntelligentTieringConfiguration, typing.Dict[str, typing.Any]]]] = None,
                inventories: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.Inventory, typing.Dict[str, typing.Any]]]] = None,
                lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.LifecycleRule, typing.Dict[str, typing.Any]]]] = None,
                metrics: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.BucketMetrics, typing.Dict[str, typing.Any]]]] = None,
                notifications_handler_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
                object_ownership: typing.Optional[aws_cdk.aws_s3.ObjectOwnership] = None,
                public_read_access: typing.Optional[builtins.bool] = None,
                removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
                server_access_logs_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
                server_access_logs_prefix: typing.Optional[builtins.str] = None,
                transfer_acceleration: typing.Optional[builtins.bool] = None,
                versioned: typing.Optional[builtins.bool] = None,
                website_error_document: typing.Optional[builtins.str] = None,
                website_index_document: typing.Optional[builtins.str] = None,
                website_redirect: typing.Optional[typing.Union[aws_cdk.aws_s3.RedirectTarget, typing.Dict[str, typing.Any]]] = None,
                website_routing_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.RoutingRule, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_s3.BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            notifications_handler_role=notifications_handler_role,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: aws_cdk.aws_s3.Bucket) -> None:
        if __debug__:
            def stub(value: aws_cdk.aws_s3.Bucket) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)


__all__ = [
    "SecureBucket",
]

publication.publish()
