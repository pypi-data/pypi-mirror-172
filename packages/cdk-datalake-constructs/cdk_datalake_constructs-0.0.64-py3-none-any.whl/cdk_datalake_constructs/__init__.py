'''
# cdk-datalake-constructs  <!-- omit in toc -->

***Very experimental until version 1.0.***
This is my attempt at simplifying deploying various datalake strategies in AWS with the CDK.

[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Build](https://github.com/randyridgley/cdk-datalake-constructs/workflows/build/badge.svg)](https://github.com/randyridgley/cdk-datalake-constructs/workflows/build.yml)
[![Release](https://github.com/randyridgley/cdk-datalake-constructs/workflows/release/badge.svg)](https://github.com/randyridgley/cdk-datalake-constructs/workflows/release.yml)
[![Python](https://img.shields.io/pypi/pyversions/cdk-datalake-constructs)](https://pypi.org) [![pip](https://img.shields.io/badge/pip%20install-cdk--datalake--constructs-blue)](https://pypi.org/project/cdk-datalake-constructs/)
[![npm version](https://img.shields.io/npm/v/cdk-datalake-constructs)](https://www.npmjs.com/package/@randyridgley/cdk-datalake-constructs) [![pypi version](https://img.shields.io/pypi/v/cdk-datalake-constructs)](https://pypi.org/project/cdk-datalake-constructs/) [![Maven](https://img.shields.io/maven-central/v/io.github.randyridgley/cdk-datalake-constructs)](https://search.maven.org/search?q=a:cdk-datalake-constructs) [![nuget](https://img.shields.io/nuget/v/Cdk.Datalake.Constructs)](https://www.nuget.org/packages/Cdk.Datalake.Constructs/)

**Table of Contents**

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)

  * [Basic](#basic)
  * [Data Mesh](#data-mesh)
* [Documentation](#documentation)

  * [Construct API Reference](#construct-api-reference)
* [Supporting this project](#supporting-this-project)
* [License](#license)

## Features

* Easy to Start - Create a Datalake in a few lines.
* Easy to Expand - Expand into multiple accounts and into a data mesh.
* Easy to Admin - Initial governance created on deploy.

## Installation

TypeScript/JavaScript

```sh
$ npm install @randyridgley/cdk-datalake-constructs
```

Python

```sh
$ pip install cdk-datalake-constructs
```

.Net

```sh
$ nuget install CDK.Datalake.Constructs

# See more: https://www.nuget.org/packages/CDK.Datalake.Constructs/
```

## Usage

### Basic

```python
import { DataLake } from '@randyridgley/cdk-datalake-constructs';

const taxiPipes: Array<dl.Pipeline> = [
  pipelines.YellowPipeline(),
  pipelines.GreenPipeline(),
]

const dataProducts: Array<dl.DataProduct> = [{
  pipelines: taxiPipes,
  accountId: lakeAccountId,
  dataCatalogAccountId: '123456789012',
  databaseName: 'taxi-product'
}]

// deploy to local account
new dl.DataLake(this, 'LocalDataLake', {
  name: 'data-lake',
  accountId: centralAccountId,
  region: 'us-east-1',
  policyTags: {
    "classification": "public,confidential,highlyconfidential,restricted,critical",
    "owner": "product,central,consumer"
  },
  stageName: Stage.PROD,
  dataProducts: dataProducts,
  createDefaultDatabase: false
});
```

### Data Mesh

You can setup cross account access and pre-created policy tags for TBAC access in Lake Formation

```python
const lakeAccountId = app.node.tryGetContext('lakeAccountId')
const centralAccountId = app.node.tryGetContext('centralAccountId')
const consumerAccountId = app.node.tryGetContext('consumerAccountId')

const taxiPipes: Array<dl.Pipeline> = [
  pipelines.YellowPipeline(),
  pipelines.GreenPipeline(),
]

const dataProducts: Array<dl.DataProduct> = [{
  pipelines: taxiPipes,
  accountId: lakeAccountId,
  dataCatalogAccountId: centralAccountId,
  databaseName: 'taxi-product'
}]

// deploy to the central account
new dl.DataLake(this, 'CentralDataLake', {
  name: 'central-lake',
  accountId: centralAccountId,
  region: 'us-east-1',
  policyTags: {
    "classification": "public,confidential,highlyconfidential,restricted,critical",
    "owner": "product,central,consumer"
  },
  stageName: Stage.PROD,
  crossAccount: {
    consumerAccountIds: [consumerAccountId, lakeAccountId],
    dataCatalogOwnerAccountId: centralAccountId,
    region: 'us-east-1', // this is still only single region today
  },
  dataProducts: dataProducts,
  createDefaultDatabase: true
});

// deploy to the data product account
const datalake = new dl.DataLake(this, 'LocalDataLake', {
  name: 'local-lake',
  accountId: lakeAccountId,
  region: 'us-east-1',
  stageName: Stage.PROD,
  dataProducts: dataProducts,
  createDefaultDatabase: true
});

// Optionally add custom resource to download public data set products
datalake.createDownloaderCustomResource(accountId, region, props.stageName)

// deploy to consumer account
const datalake = new dl.DataLake(this, 'ConsumerDataLake', {
  name: 'consumer-lake',
  accountId: consumerAccountId,
  region: 'us-east-1',
  stageName: Stage.PROD,
  policyTags: {
    "access": "analyst,engineer,marketing"
  },
  createDefaultDatabase: true
});
```

## Documentation

### Construct API Reference

See [API.md](./API.md).

## Supporting this project

I'm working on this project in my free time, if you like my project, or found it helpful and would like to support me any contributions are much appreciated! ❤️

## License

This project is distributed under the [MIT](./LICENSE).
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
import aws_cdk.aws_athena
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_events
import aws_cdk.aws_glue
import aws_cdk.aws_glue_alpha
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import constructs


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.CompressionType")
class CompressionType(enum.Enum):
    UNCOMPRESSED = "UNCOMPRESSED"
    GZIP = "GZIP"
    ZIP = "ZIP"
    SNAPPY = "SNAPPY"


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.CrossAccountProperties",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_account_ids": "consumerAccountIds",
        "data_catalog_owner_account_id": "dataCatalogOwnerAccountId",
    },
)
class CrossAccountProperties:
    def __init__(
        self,
        *,
        consumer_account_ids: typing.Sequence[builtins.str],
        data_catalog_owner_account_id: builtins.str,
    ) -> None:
        '''
        :param consumer_account_ids: 
        :param data_catalog_owner_account_id: 
        '''
        if __debug__:
            def stub(
                *,
                consumer_account_ids: typing.Sequence[builtins.str],
                data_catalog_owner_account_id: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument consumer_account_ids", value=consumer_account_ids, expected_type=type_hints["consumer_account_ids"])
            check_type(argname="argument data_catalog_owner_account_id", value=data_catalog_owner_account_id, expected_type=type_hints["data_catalog_owner_account_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "consumer_account_ids": consumer_account_ids,
            "data_catalog_owner_account_id": data_catalog_owner_account_id,
        }

    @builtins.property
    def consumer_account_ids(self) -> typing.List[builtins.str]:
        result = self._values.get("consumer_account_ids")
        assert result is not None, "Required property 'consumer_account_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def data_catalog_owner_account_id(self) -> builtins.str:
        result = self._values.get("data_catalog_owner_account_id")
        assert result is not None, "Required property 'data_catalog_owner_account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossAccountProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataCatalogOwner",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class DataCatalogOwner:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: 
        '''
        if __debug__:
            def stub(*, account_id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogOwner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLake(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLake",
):
    '''A CDK construct to create a DataLake.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        lake_kind: "LakeKind",
        name: builtins.str,
        stage_name: "Stage",
        create_athena_workgroup: typing.Optional[builtins.bool] = None,
        create_default_databse: typing.Optional[builtins.bool] = None,
        cross_account_access: typing.Optional[typing.Union[CrossAccountProperties, typing.Dict[str, typing.Any]]] = None,
        datalake_admin_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        datalake_creator_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        data_products: typing.Optional[typing.Sequence["DataProduct"]] = None,
        glue_security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
        log_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
        policy_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lake_kind: The Type of DataLake this instance is. This can be a DATA_PRODUCT only, CENTRAL_CATALOG, CONSUMER, or DATA_PRODUCT_AND_CATALOG type.
        :param name: The name of the DataLake.
        :param stage_name: The Stage the DataLake will be deployed.
        :param create_athena_workgroup: Create default Athena workgroup for querying data lake resources. Default: - false
        :param create_default_databse: Create default glue database for the data lake. Default: false
        :param cross_account_access: Cross account AWS account IDs. Default: - No cross account ids
        :param datalake_admin_role: Data Lake Admin role. Default: - Admin role created based on best practices
        :param datalake_creator_role: Data Lake Database Creator role. Default: - Database creator role created based on best practices
        :param data_products: The List of DataProducts for this account. Default: - No data products
        :param glue_security_group: Security group to attach to Glue jobs. Default: - No security group
        :param log_bucket_props: 
        :param policy_tags: List of Lake Formation TBAC policy tags. Default: - No tags
        :param vpc: VPC for Glue jobs. Default: - No vpc
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                lake_kind: "LakeKind",
                name: builtins.str,
                stage_name: "Stage",
                create_athena_workgroup: typing.Optional[builtins.bool] = None,
                create_default_databse: typing.Optional[builtins.bool] = None,
                cross_account_access: typing.Optional[typing.Union[CrossAccountProperties, typing.Dict[str, typing.Any]]] = None,
                datalake_admin_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
                datalake_creator_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
                data_products: typing.Optional[typing.Sequence["DataProduct"]] = None,
                glue_security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
                log_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
                policy_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeProperties(
            lake_kind=lake_kind,
            name=name,
            stage_name=stage_name,
            create_athena_workgroup=create_athena_workgroup,
            create_default_databse=create_default_databse,
            cross_account_access=cross_account_access,
            datalake_admin_role=datalake_admin_role,
            datalake_creator_role=datalake_creator_role,
            data_products=data_products,
            glue_security_group=glue_security_group,
            log_bucket_props=log_bucket_props,
            policy_tags=policy_tags,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createCrossAccountGlueCatalogResourcePolicy")
    def _create_cross_account_glue_catalog_resource_policy(
        self,
        consumer_account_ids: typing.Sequence[builtins.str],
        data_catalog_owner_account_id: builtins.str,
    ) -> None:
        '''
        :param consumer_account_ids: -
        :param data_catalog_owner_account_id: -
        '''
        if __debug__:
            def stub(
                consumer_account_ids: typing.Sequence[builtins.str],
                data_catalog_owner_account_id: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument consumer_account_ids", value=consumer_account_ids, expected_type=type_hints["consumer_account_ids"])
            check_type(argname="argument data_catalog_owner_account_id", value=data_catalog_owner_account_id, expected_type=type_hints["data_catalog_owner_account_id"])
        return typing.cast(None, jsii.invoke(self, "createCrossAccountGlueCatalogResourcePolicy", [consumer_account_ids, data_catalog_owner_account_id]))

    @jsii.member(jsii_name="createDownloaderCustomResource")
    def create_downloader_custom_resource(self, stage_name: builtins.str) -> None:
        '''
        :param stage_name: -
        '''
        if __debug__:
            def stub(stage_name: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        return typing.cast(None, jsii.invoke(self, "createDownloaderCustomResource", [stage_name]))

    @builtins.property
    @jsii.member(jsii_name="databases")
    def databases(
        self,
    ) -> typing.Mapping[builtins.str, aws_cdk.aws_glue_alpha.Database]:
        return typing.cast(typing.Mapping[builtins.str, aws_cdk.aws_glue_alpha.Database], jsii.get(self, "databases"))

    @builtins.property
    @jsii.member(jsii_name="datalakeAdminRole")
    def datalake_admin_role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "datalakeAdminRole"))

    @builtins.property
    @jsii.member(jsii_name="datalakeDbCreatorRole")
    def datalake_db_creator_role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "datalakeDbCreatorRole"))

    @builtins.property
    @jsii.member(jsii_name="lakeKind")
    def lake_kind(self) -> "LakeKind":
        return typing.cast("LakeKind", jsii.get(self, "lakeKind"))

    @builtins.property
    @jsii.member(jsii_name="logBucket")
    def log_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "logBucket"))

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> "Stage":
        return typing.cast("Stage", jsii.get(self, "stageName"))

    @builtins.property
    @jsii.member(jsii_name="athenaWorkgroup")
    def athena_workgroup(self) -> typing.Optional[aws_cdk.aws_athena.CfnWorkGroup]:
        return typing.cast(typing.Optional[aws_cdk.aws_athena.CfnWorkGroup], jsii.get(self, "athenaWorkgroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.Vpc]:
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.Vpc], jsii.get(self, "vpc"))


class DataLakeAdministrator(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeAdministrator",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                name: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeAdministratorProps(name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeAdministratorProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLakeAdministratorProps:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        if __debug__:
            def stub(*, name: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeAdministratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeAnalyst(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeAnalyst",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param read_access_buckets: 
        :param write_access_buckets: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                name: builtins.str,
                read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
                write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeAnalystProps(
            name=name,
            read_access_buckets=read_access_buckets,
            write_access_buckets=write_access_buckets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> aws_cdk.aws_iam.User:
        return typing.cast(aws_cdk.aws_iam.User, jsii.get(self, "user"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeAnalystProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "read_access_buckets": "readAccessBuckets",
        "write_access_buckets": "writeAccessBuckets",
    },
)
class DataLakeAnalystProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
    ) -> None:
        '''
        :param name: 
        :param read_access_buckets: 
        :param write_access_buckets: 
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
                write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument read_access_buckets", value=read_access_buckets, expected_type=type_hints["read_access_buckets"])
            check_type(argname="argument write_access_buckets", value=write_access_buckets, expected_type=type_hints["write_access_buckets"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if read_access_buckets is not None:
            self._values["read_access_buckets"] = read_access_buckets
        if write_access_buckets is not None:
            self._values["write_access_buckets"] = write_access_buckets

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("read_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    @builtins.property
    def write_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("write_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeAnalystProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeBucket(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        cross_account: builtins.bool,
        data_catalog_account_id: builtins.str,
        log_bucket: aws_cdk.aws_s3.Bucket,
        s3_properties: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param cross_account: 
        :param data_catalog_account_id: 
        :param log_bucket: 
        :param s3_properties: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                bucket_name: builtins.str,
                cross_account: builtins.bool,
                data_catalog_account_id: builtins.str,
                log_bucket: aws_cdk.aws_s3.Bucket,
                s3_properties: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeBucketProps(
            bucket_name=bucket_name,
            cross_account=cross_account,
            data_catalog_account_id=data_catalog_account_id,
            log_bucket=log_bucket,
            s3_properties=s3_properties,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "bucket"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "cross_account": "crossAccount",
        "data_catalog_account_id": "dataCatalogAccountId",
        "log_bucket": "logBucket",
        "s3_properties": "s3Properties",
    },
)
class DataLakeBucketProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        cross_account: builtins.bool,
        data_catalog_account_id: builtins.str,
        log_bucket: aws_cdk.aws_s3.Bucket,
        s3_properties: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param cross_account: 
        :param data_catalog_account_id: 
        :param log_bucket: 
        :param s3_properties: 
        '''
        if isinstance(s3_properties, dict):
            s3_properties = aws_cdk.aws_s3.BucketProps(**s3_properties)
        if __debug__:
            def stub(
                *,
                bucket_name: builtins.str,
                cross_account: builtins.bool,
                data_catalog_account_id: builtins.str,
                log_bucket: aws_cdk.aws_s3.Bucket,
                s3_properties: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cross_account", value=cross_account, expected_type=type_hints["cross_account"])
            check_type(argname="argument data_catalog_account_id", value=data_catalog_account_id, expected_type=type_hints["data_catalog_account_id"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument s3_properties", value=s3_properties, expected_type=type_hints["s3_properties"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
            "cross_account": cross_account,
            "data_catalog_account_id": data_catalog_account_id,
            "log_bucket": log_bucket,
        }
        if s3_properties is not None:
            self._values["s3_properties"] = s3_properties

    @builtins.property
    def bucket_name(self) -> builtins.str:
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_account(self) -> builtins.bool:
        result = self._values.get("cross_account")
        assert result is not None, "Required property 'cross_account' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def data_catalog_account_id(self) -> builtins.str:
        result = self._values.get("data_catalog_account_id")
        assert result is not None, "Required property 'data_catalog_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_bucket(self) -> aws_cdk.aws_s3.Bucket:
        result = self._values.get("log_bucket")
        assert result is not None, "Required property 'log_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def s3_properties(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        result = self._values.get("s3_properties")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeCreator(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeCreator",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                name: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeCreatorProperties(name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeCreatorProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLakeCreatorProperties:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        if __debug__:
            def stub(*, name: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeCreatorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataLakeProperties",
    jsii_struct_bases=[],
    name_mapping={
        "lake_kind": "lakeKind",
        "name": "name",
        "stage_name": "stageName",
        "create_athena_workgroup": "createAthenaWorkgroup",
        "create_default_databse": "createDefaultDatabse",
        "cross_account_access": "crossAccountAccess",
        "datalake_admin_role": "datalakeAdminRole",
        "datalake_creator_role": "datalakeCreatorRole",
        "data_products": "dataProducts",
        "glue_security_group": "glueSecurityGroup",
        "log_bucket_props": "logBucketProps",
        "policy_tags": "policyTags",
        "vpc": "vpc",
    },
)
class DataLakeProperties:
    def __init__(
        self,
        *,
        lake_kind: "LakeKind",
        name: builtins.str,
        stage_name: "Stage",
        create_athena_workgroup: typing.Optional[builtins.bool] = None,
        create_default_databse: typing.Optional[builtins.bool] = None,
        cross_account_access: typing.Optional[typing.Union[CrossAccountProperties, typing.Dict[str, typing.Any]]] = None,
        datalake_admin_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        datalake_creator_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        data_products: typing.Optional[typing.Sequence["DataProduct"]] = None,
        glue_security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
        log_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
        policy_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
    ) -> None:
        '''
        :param lake_kind: The Type of DataLake this instance is. This can be a DATA_PRODUCT only, CENTRAL_CATALOG, CONSUMER, or DATA_PRODUCT_AND_CATALOG type.
        :param name: The name of the DataLake.
        :param stage_name: The Stage the DataLake will be deployed.
        :param create_athena_workgroup: Create default Athena workgroup for querying data lake resources. Default: - false
        :param create_default_databse: Create default glue database for the data lake. Default: false
        :param cross_account_access: Cross account AWS account IDs. Default: - No cross account ids
        :param datalake_admin_role: Data Lake Admin role. Default: - Admin role created based on best practices
        :param datalake_creator_role: Data Lake Database Creator role. Default: - Database creator role created based on best practices
        :param data_products: The List of DataProducts for this account. Default: - No data products
        :param glue_security_group: Security group to attach to Glue jobs. Default: - No security group
        :param log_bucket_props: 
        :param policy_tags: List of Lake Formation TBAC policy tags. Default: - No tags
        :param vpc: VPC for Glue jobs. Default: - No vpc
        '''
        if isinstance(cross_account_access, dict):
            cross_account_access = CrossAccountProperties(**cross_account_access)
        if isinstance(log_bucket_props, dict):
            log_bucket_props = aws_cdk.aws_s3.BucketProps(**log_bucket_props)
        if __debug__:
            def stub(
                *,
                lake_kind: "LakeKind",
                name: builtins.str,
                stage_name: "Stage",
                create_athena_workgroup: typing.Optional[builtins.bool] = None,
                create_default_databse: typing.Optional[builtins.bool] = None,
                cross_account_access: typing.Optional[typing.Union[CrossAccountProperties, typing.Dict[str, typing.Any]]] = None,
                datalake_admin_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
                datalake_creator_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
                data_products: typing.Optional[typing.Sequence["DataProduct"]] = None,
                glue_security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
                log_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
                policy_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                vpc: typing.Optional[aws_cdk.aws_ec2.Vpc] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument lake_kind", value=lake_kind, expected_type=type_hints["lake_kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument create_athena_workgroup", value=create_athena_workgroup, expected_type=type_hints["create_athena_workgroup"])
            check_type(argname="argument create_default_databse", value=create_default_databse, expected_type=type_hints["create_default_databse"])
            check_type(argname="argument cross_account_access", value=cross_account_access, expected_type=type_hints["cross_account_access"])
            check_type(argname="argument datalake_admin_role", value=datalake_admin_role, expected_type=type_hints["datalake_admin_role"])
            check_type(argname="argument datalake_creator_role", value=datalake_creator_role, expected_type=type_hints["datalake_creator_role"])
            check_type(argname="argument data_products", value=data_products, expected_type=type_hints["data_products"])
            check_type(argname="argument glue_security_group", value=glue_security_group, expected_type=type_hints["glue_security_group"])
            check_type(argname="argument log_bucket_props", value=log_bucket_props, expected_type=type_hints["log_bucket_props"])
            check_type(argname="argument policy_tags", value=policy_tags, expected_type=type_hints["policy_tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "lake_kind": lake_kind,
            "name": name,
            "stage_name": stage_name,
        }
        if create_athena_workgroup is not None:
            self._values["create_athena_workgroup"] = create_athena_workgroup
        if create_default_databse is not None:
            self._values["create_default_databse"] = create_default_databse
        if cross_account_access is not None:
            self._values["cross_account_access"] = cross_account_access
        if datalake_admin_role is not None:
            self._values["datalake_admin_role"] = datalake_admin_role
        if datalake_creator_role is not None:
            self._values["datalake_creator_role"] = datalake_creator_role
        if data_products is not None:
            self._values["data_products"] = data_products
        if glue_security_group is not None:
            self._values["glue_security_group"] = glue_security_group
        if log_bucket_props is not None:
            self._values["log_bucket_props"] = log_bucket_props
        if policy_tags is not None:
            self._values["policy_tags"] = policy_tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def lake_kind(self) -> "LakeKind":
        '''The Type of DataLake this instance is.

        This can be a DATA_PRODUCT only, CENTRAL_CATALOG, CONSUMER, or DATA_PRODUCT_AND_CATALOG type.
        '''
        result = self._values.get("lake_kind")
        assert result is not None, "Required property 'lake_kind' is missing"
        return typing.cast("LakeKind", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the DataLake.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_name(self) -> "Stage":
        '''The Stage the DataLake will be deployed.'''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast("Stage", result)

    @builtins.property
    def create_athena_workgroup(self) -> typing.Optional[builtins.bool]:
        '''Create default Athena workgroup for querying data lake resources.

        :default: - false
        '''
        result = self._values.get("create_athena_workgroup")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def create_default_databse(self) -> typing.Optional[builtins.bool]:
        '''Create default glue database for the data lake.

        :default: false
        '''
        result = self._values.get("create_default_databse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_account_access(self) -> typing.Optional[CrossAccountProperties]:
        '''Cross account AWS account IDs.

        :default: - No cross account ids

        :see: https://aws.amazon.com/premiumsupport/knowledge-center/glue-data-catalog-cross-account-access/
        :description: - The cross account ids needed for setting up the Glue resource policy
        '''
        result = self._values.get("cross_account_access")
        return typing.cast(typing.Optional[CrossAccountProperties], result)

    @builtins.property
    def datalake_admin_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        '''Data Lake Admin role.

        :default: - Admin role created based on best practices

        :see: https://docs.aws.amazon.com/lake-formation/latest/dg/permissions-reference.html
        :description: - IAM Role for DataLake admin access
        '''
        result = self._values.get("datalake_admin_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.Role], result)

    @builtins.property
    def datalake_creator_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        '''Data Lake Database Creator role.

        :default: - Database creator role created based on best practices

        :see: https://docs.aws.amazon.com/lake-formation/latest/dg/permissions-reference.html
        :description: - IAM Role for DataLake database creator access
        '''
        result = self._values.get("datalake_creator_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.Role], result)

    @builtins.property
    def data_products(self) -> typing.Optional[typing.List["DataProduct"]]:
        '''The List of DataProducts for this account.

        :default: - No data products
        '''
        result = self._values.get("data_products")
        return typing.cast(typing.Optional[typing.List["DataProduct"]], result)

    @builtins.property
    def glue_security_group(self) -> typing.Optional[aws_cdk.aws_ec2.SecurityGroup]:
        '''Security group to attach to Glue jobs.

        :default: - No security group

        :see: https://docs.aws.amazon.com/glue/latest/dg/setup-vpc-for-glue-access.html
        :description: - Security Group that will be used to allow port access in the VPC
        '''
        result = self._values.get("glue_security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SecurityGroup], result)

    @builtins.property
    def log_bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        result = self._values.get("log_bucket_props")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    @builtins.property
    def policy_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''List of Lake Formation TBAC policy tags.

        :default: - No tags

        :see: https://docs.aws.amazon.com/lake-formation/latest/dg/TBAC-section.html
        :description: - Define the tag taxonomy needed for the DataLake
        '''
        result = self._values.get("policy_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.Vpc]:
        '''VPC for Glue jobs.

        :default: - No vpc

        :description: - The VPC that will be used if the Glue job needs access to resources within the account or internet access
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.Vpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.DataPipelineType")
class DataPipelineType(enum.Enum):
    STREAM = "STREAM"
    JDBC = "JDBC"
    S3 = "S3"


@jsii.implements(constructs.IDependable)
class DataProduct(
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.DataProduct",
):
    def __init__(
        self,
        *,
        account_id: builtins.str,
        database_name: builtins.str,
        pipelines: typing.Sequence["Pipeline"],
        data_catalog_account_id: typing.Optional[builtins.str] = None,
        s3_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_id: 
        :param database_name: 
        :param pipelines: 
        :param data_catalog_account_id: 
        :param s3_bucket_props: 
        '''
        props = DataProductProperties(
            account_id=account_id,
            database_name=database_name,
            pipelines=pipelines,
            data_catalog_account_id=data_catalog_account_id,
            s3_bucket_props=s3_bucket_props,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="pipelines")
    def pipelines(self) -> typing.List["Pipeline"]:
        return typing.cast(typing.List["Pipeline"], jsii.get(self, "pipelines"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogAccountId")
    def data_catalog_account_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCatalogAccountId"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketProps")
    def s3_bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], jsii.get(self, "s3BucketProps"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataProductProperties",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "database_name": "databaseName",
        "pipelines": "pipelines",
        "data_catalog_account_id": "dataCatalogAccountId",
        "s3_bucket_props": "s3BucketProps",
    },
)
class DataProductProperties:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        database_name: builtins.str,
        pipelines: typing.Sequence["Pipeline"],
        data_catalog_account_id: typing.Optional[builtins.str] = None,
        s3_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_id: 
        :param database_name: 
        :param pipelines: 
        :param data_catalog_account_id: 
        :param s3_bucket_props: 
        '''
        if isinstance(s3_bucket_props, dict):
            s3_bucket_props = aws_cdk.aws_s3.BucketProps(**s3_bucket_props)
        if __debug__:
            def stub(
                *,
                account_id: builtins.str,
                database_name: builtins.str,
                pipelines: typing.Sequence["Pipeline"],
                data_catalog_account_id: typing.Optional[builtins.str] = None,
                s3_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument pipelines", value=pipelines, expected_type=type_hints["pipelines"])
            check_type(argname="argument data_catalog_account_id", value=data_catalog_account_id, expected_type=type_hints["data_catalog_account_id"])
            check_type(argname="argument s3_bucket_props", value=s3_bucket_props, expected_type=type_hints["s3_bucket_props"])
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "database_name": database_name,
            "pipelines": pipelines,
        }
        if data_catalog_account_id is not None:
            self._values["data_catalog_account_id"] = data_catalog_account_id
        if s3_bucket_props is not None:
            self._values["s3_bucket_props"] = s3_bucket_props

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipelines(self) -> typing.List["Pipeline"]:
        result = self._values.get("pipelines")
        assert result is not None, "Required property 'pipelines' is missing"
        return typing.cast(typing.List["Pipeline"], result)

    @builtins.property
    def data_catalog_account_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("data_catalog_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        result = self._values.get("s3_bucket_props")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProductProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataSetResult",
    jsii_struct_bases=[],
    name_mapping={
        "destination_bucket_name": "destinationBucketName",
        "destination_prefix": "destinationPrefix",
        "raw_bucket_name": "rawBucketName",
        "refined_bucket_name": "refinedBucketName",
        "trusted_bucket_name": "trustedBucketName",
        "source_bucket_name": "sourceBucketName",
        "source_keys": "sourceKeys",
    },
)
class DataSetResult:
    def __init__(
        self,
        *,
        destination_bucket_name: builtins.str,
        destination_prefix: builtins.str,
        raw_bucket_name: builtins.str,
        refined_bucket_name: builtins.str,
        trusted_bucket_name: builtins.str,
        source_bucket_name: typing.Optional[builtins.str] = None,
        source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param destination_bucket_name: 
        :param destination_prefix: 
        :param raw_bucket_name: 
        :param refined_bucket_name: 
        :param trusted_bucket_name: 
        :param source_bucket_name: 
        :param source_keys: 
        '''
        if __debug__:
            def stub(
                *,
                destination_bucket_name: builtins.str,
                destination_prefix: builtins.str,
                raw_bucket_name: builtins.str,
                refined_bucket_name: builtins.str,
                trusted_bucket_name: builtins.str,
                source_bucket_name: typing.Optional[builtins.str] = None,
                source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument destination_bucket_name", value=destination_bucket_name, expected_type=type_hints["destination_bucket_name"])
            check_type(argname="argument destination_prefix", value=destination_prefix, expected_type=type_hints["destination_prefix"])
            check_type(argname="argument raw_bucket_name", value=raw_bucket_name, expected_type=type_hints["raw_bucket_name"])
            check_type(argname="argument refined_bucket_name", value=refined_bucket_name, expected_type=type_hints["refined_bucket_name"])
            check_type(argname="argument trusted_bucket_name", value=trusted_bucket_name, expected_type=type_hints["trusted_bucket_name"])
            check_type(argname="argument source_bucket_name", value=source_bucket_name, expected_type=type_hints["source_bucket_name"])
            check_type(argname="argument source_keys", value=source_keys, expected_type=type_hints["source_keys"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination_bucket_name": destination_bucket_name,
            "destination_prefix": destination_prefix,
            "raw_bucket_name": raw_bucket_name,
            "refined_bucket_name": refined_bucket_name,
            "trusted_bucket_name": trusted_bucket_name,
        }
        if source_bucket_name is not None:
            self._values["source_bucket_name"] = source_bucket_name
        if source_keys is not None:
            self._values["source_keys"] = source_keys

    @builtins.property
    def destination_bucket_name(self) -> builtins.str:
        result = self._values.get("destination_bucket_name")
        assert result is not None, "Required property 'destination_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_prefix(self) -> builtins.str:
        result = self._values.get("destination_prefix")
        assert result is not None, "Required property 'destination_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def raw_bucket_name(self) -> builtins.str:
        result = self._values.get("raw_bucket_name")
        assert result is not None, "Required property 'raw_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def refined_bucket_name(self) -> builtins.str:
        result = self._values.get("refined_bucket_name")
        assert result is not None, "Required property 'refined_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trusted_bucket_name(self) -> builtins.str:
        result = self._values.get("trusted_bucket_name")
        assert result is not None, "Required property 'trusted_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("source_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("source_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSetResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataStreamProperties",
    jsii_struct_bases=[],
    name_mapping={
        "data_catalog_owner": "dataCatalogOwner",
        "destination_bucket_name": "destinationBucketName",
        "destination_prefix": "destinationPrefix",
        "lambda_data_generator": "lambdaDataGenerator",
        "name": "name",
        "stream_name": "streamName",
    },
)
class DataStreamProperties:
    def __init__(
        self,
        *,
        data_catalog_owner: typing.Union[DataCatalogOwner, typing.Dict[str, typing.Any]],
        destination_bucket_name: builtins.str,
        destination_prefix: builtins.str,
        lambda_data_generator: typing.Union["LambdaDataGeneratorProperties", typing.Dict[str, typing.Any]],
        name: builtins.str,
        stream_name: builtins.str,
    ) -> None:
        '''
        :param data_catalog_owner: 
        :param destination_bucket_name: 
        :param destination_prefix: 
        :param lambda_data_generator: 
        :param name: 
        :param stream_name: 
        '''
        if isinstance(data_catalog_owner, dict):
            data_catalog_owner = DataCatalogOwner(**data_catalog_owner)
        if isinstance(lambda_data_generator, dict):
            lambda_data_generator = LambdaDataGeneratorProperties(**lambda_data_generator)
        if __debug__:
            def stub(
                *,
                data_catalog_owner: typing.Union[DataCatalogOwner, typing.Dict[str, typing.Any]],
                destination_bucket_name: builtins.str,
                destination_prefix: builtins.str,
                lambda_data_generator: typing.Union["LambdaDataGeneratorProperties", typing.Dict[str, typing.Any]],
                name: builtins.str,
                stream_name: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument data_catalog_owner", value=data_catalog_owner, expected_type=type_hints["data_catalog_owner"])
            check_type(argname="argument destination_bucket_name", value=destination_bucket_name, expected_type=type_hints["destination_bucket_name"])
            check_type(argname="argument destination_prefix", value=destination_prefix, expected_type=type_hints["destination_prefix"])
            check_type(argname="argument lambda_data_generator", value=lambda_data_generator, expected_type=type_hints["lambda_data_generator"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "data_catalog_owner": data_catalog_owner,
            "destination_bucket_name": destination_bucket_name,
            "destination_prefix": destination_prefix,
            "lambda_data_generator": lambda_data_generator,
            "name": name,
            "stream_name": stream_name,
        }

    @builtins.property
    def data_catalog_owner(self) -> DataCatalogOwner:
        result = self._values.get("data_catalog_owner")
        assert result is not None, "Required property 'data_catalog_owner' is missing"
        return typing.cast(DataCatalogOwner, result)

    @builtins.property
    def destination_bucket_name(self) -> builtins.str:
        result = self._values.get("destination_bucket_name")
        assert result is not None, "Required property 'destination_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_prefix(self) -> builtins.str:
        result = self._values.get("destination_prefix")
        assert result is not None, "Required property 'destination_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_data_generator(self) -> "LambdaDataGeneratorProperties":
        result = self._values.get("lambda_data_generator")
        assert result is not None, "Required property 'lambda_data_generator' is missing"
        return typing.cast("LambdaDataGeneratorProperties", result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataStreamProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.DataTier")
class DataTier(enum.Enum):
    RAW = "RAW"
    REFINED = "REFINED"
    TRUSTED = "TRUSTED"


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DataTierBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "cross_account": "crossAccount",
        "data_catalog_account_id": "dataCatalogAccountId",
        "datalake_admin_role": "datalakeAdminRole",
        "datalake_db_creator_role": "datalakeDbCreatorRole",
        "lake_type": "lakeType",
        "log_bucket": "logBucket",
        "pipeline_name": "pipelineName",
        "tier": "tier",
        "bucket_name": "bucketName",
        "s3_bucket_props": "s3BucketProps",
    },
)
class DataTierBucketProps:
    def __init__(
        self,
        *,
        cross_account: builtins.bool,
        data_catalog_account_id: builtins.str,
        datalake_admin_role: aws_cdk.aws_iam.IRole,
        datalake_db_creator_role: aws_cdk.aws_iam.IRole,
        lake_type: "LakeKind",
        log_bucket: aws_cdk.aws_s3.Bucket,
        pipeline_name: builtins.str,
        tier: DataTier,
        bucket_name: typing.Optional[builtins.str] = None,
        s3_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cross_account: 
        :param data_catalog_account_id: 
        :param datalake_admin_role: 
        :param datalake_db_creator_role: 
        :param lake_type: 
        :param log_bucket: 
        :param pipeline_name: 
        :param tier: 
        :param bucket_name: 
        :param s3_bucket_props: 
        '''
        if isinstance(s3_bucket_props, dict):
            s3_bucket_props = aws_cdk.aws_s3.BucketProps(**s3_bucket_props)
        if __debug__:
            def stub(
                *,
                cross_account: builtins.bool,
                data_catalog_account_id: builtins.str,
                datalake_admin_role: aws_cdk.aws_iam.IRole,
                datalake_db_creator_role: aws_cdk.aws_iam.IRole,
                lake_type: "LakeKind",
                log_bucket: aws_cdk.aws_s3.Bucket,
                pipeline_name: builtins.str,
                tier: DataTier,
                bucket_name: typing.Optional[builtins.str] = None,
                s3_bucket_props: typing.Optional[typing.Union[aws_cdk.aws_s3.BucketProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cross_account", value=cross_account, expected_type=type_hints["cross_account"])
            check_type(argname="argument data_catalog_account_id", value=data_catalog_account_id, expected_type=type_hints["data_catalog_account_id"])
            check_type(argname="argument datalake_admin_role", value=datalake_admin_role, expected_type=type_hints["datalake_admin_role"])
            check_type(argname="argument datalake_db_creator_role", value=datalake_db_creator_role, expected_type=type_hints["datalake_db_creator_role"])
            check_type(argname="argument lake_type", value=lake_type, expected_type=type_hints["lake_type"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument s3_bucket_props", value=s3_bucket_props, expected_type=type_hints["s3_bucket_props"])
        self._values: typing.Dict[str, typing.Any] = {
            "cross_account": cross_account,
            "data_catalog_account_id": data_catalog_account_id,
            "datalake_admin_role": datalake_admin_role,
            "datalake_db_creator_role": datalake_db_creator_role,
            "lake_type": lake_type,
            "log_bucket": log_bucket,
            "pipeline_name": pipeline_name,
            "tier": tier,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if s3_bucket_props is not None:
            self._values["s3_bucket_props"] = s3_bucket_props

    @builtins.property
    def cross_account(self) -> builtins.bool:
        result = self._values.get("cross_account")
        assert result is not None, "Required property 'cross_account' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def data_catalog_account_id(self) -> builtins.str:
        result = self._values.get("data_catalog_account_id")
        assert result is not None, "Required property 'data_catalog_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datalake_admin_role(self) -> aws_cdk.aws_iam.IRole:
        result = self._values.get("datalake_admin_role")
        assert result is not None, "Required property 'datalake_admin_role' is missing"
        return typing.cast(aws_cdk.aws_iam.IRole, result)

    @builtins.property
    def datalake_db_creator_role(self) -> aws_cdk.aws_iam.IRole:
        result = self._values.get("datalake_db_creator_role")
        assert result is not None, "Required property 'datalake_db_creator_role' is missing"
        return typing.cast(aws_cdk.aws_iam.IRole, result)

    @builtins.property
    def lake_type(self) -> "LakeKind":
        result = self._values.get("lake_type")
        assert result is not None, "Required property 'lake_type' is missing"
        return typing.cast("LakeKind", result)

    @builtins.property
    def log_bucket(self) -> aws_cdk.aws_s3.Bucket:
        result = self._values.get("log_bucket")
        assert result is not None, "Required property 'log_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def pipeline_name(self) -> builtins.str:
        result = self._values.get("pipeline_name")
        assert result is not None, "Required property 'pipeline_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> DataTier:
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(DataTier, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        result = self._values.get("s3_bucket_props")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTierBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.DeliveryStreamProperties",
    jsii_struct_bases=[],
    name_mapping={
        "kinesis_stream": "kinesisStream",
        "s3_bucket": "s3Bucket",
        "compression": "compression",
        "s3_prefix": "s3Prefix",
        "transform_function": "transformFunction",
    },
)
class DeliveryStreamProperties:
    def __init__(
        self,
        *,
        kinesis_stream: aws_cdk.aws_kinesis.Stream,
        s3_bucket: aws_cdk.aws_s3.IBucket,
        compression: typing.Optional[CompressionType] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        transform_function: typing.Optional[aws_cdk.aws_lambda.Function] = None,
    ) -> None:
        '''
        :param kinesis_stream: 
        :param s3_bucket: 
        :param compression: 
        :param s3_prefix: 
        :param transform_function: 
        '''
        if __debug__:
            def stub(
                *,
                kinesis_stream: aws_cdk.aws_kinesis.Stream,
                s3_bucket: aws_cdk.aws_s3.IBucket,
                compression: typing.Optional[CompressionType] = None,
                s3_prefix: typing.Optional[builtins.str] = None,
                transform_function: typing.Optional[aws_cdk.aws_lambda.Function] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            check_type(argname="argument transform_function", value=transform_function, expected_type=type_hints["transform_function"])
        self._values: typing.Dict[str, typing.Any] = {
            "kinesis_stream": kinesis_stream,
            "s3_bucket": s3_bucket,
        }
        if compression is not None:
            self._values["compression"] = compression
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix
        if transform_function is not None:
            self._values["transform_function"] = transform_function

    @builtins.property
    def kinesis_stream(self) -> aws_cdk.aws_kinesis.Stream:
        result = self._values.get("kinesis_stream")
        assert result is not None, "Required property 'kinesis_stream' is missing"
        return typing.cast(aws_cdk.aws_kinesis.Stream, result)

    @builtins.property
    def s3_bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def compression(self) -> typing.Optional[CompressionType]:
        result = self._values.get("compression")
        return typing.cast(typing.Optional[CompressionType], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_function(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        result = self._values.get("transform_function")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.Function], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.DeliveryStreamType")
class DeliveryStreamType(enum.Enum):
    DIRECT_PUT = "DIRECT_PUT"
    KINESIS_STREAM_AS_SOURCE = "KINESIS_STREAM_AS_SOURCE"


class GlueCrawler(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.GlueCrawler",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: "IGlueCrawlerProperties",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                props: "IGlueCrawlerProperties",
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metricFailure")
    def metric_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricFailure", [props]))

    @jsii.member(jsii_name="metricSuccess")
    def metric_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSuccess", [props]))

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> aws_cdk.aws_glue.CfnCrawler:
        return typing.cast(aws_cdk.aws_glue.CfnCrawler, jsii.get(self, "crawler"))

    @builtins.property
    @jsii.member(jsii_name="metricFailureRule")
    def metric_failure_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "metricFailureRule"))

    @builtins.property
    @jsii.member(jsii_name="metricSuccessRule")
    def metric_success_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "metricSuccessRule"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


class GlueJob(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.GlueJob",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        deployment_bucket: aws_cdk.aws_s3.IBucket,
        job_script: builtins.str,
        job_type: "GlueJobType",
        name: builtins.str,
        worker_type: "GlueWorkerType",
        description: typing.Optional[builtins.str] = None,
        glue_version: typing.Optional["GlueVersion"] = None,
        job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        role_name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param deployment_bucket: 
        :param job_script: 
        :param job_type: 
        :param name: 
        :param worker_type: 
        :param description: 
        :param glue_version: 
        :param job_args: 
        :param max_capacity: 
        :param max_concurrent_runs: 
        :param max_retries: 
        :param number_of_workers: 
        :param read_access_buckets: 
        :param role_name: 
        :param timeout: 
        :param write_access_buckets: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                deployment_bucket: aws_cdk.aws_s3.IBucket,
                job_script: builtins.str,
                job_type: "GlueJobType",
                name: builtins.str,
                worker_type: "GlueWorkerType",
                description: typing.Optional[builtins.str] = None,
                glue_version: typing.Optional["GlueVersion"] = None,
                job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                max_capacity: typing.Optional[jsii.Number] = None,
                max_concurrent_runs: typing.Optional[jsii.Number] = None,
                max_retries: typing.Optional[jsii.Number] = None,
                number_of_workers: typing.Optional[jsii.Number] = None,
                read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
                role_name: typing.Optional[builtins.str] = None,
                timeout: typing.Optional[jsii.Number] = None,
                write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GlueJobProperties(
            deployment_bucket=deployment_bucket,
            job_script=job_script,
            job_type=job_type,
            name=name,
            worker_type=worker_type,
            description=description,
            glue_version=glue_version,
            job_args=job_args,
            max_capacity=max_capacity,
            max_concurrent_runs=max_concurrent_runs,
            max_retries=max_retries,
            number_of_workers=number_of_workers,
            read_access_buckets=read_access_buckets,
            role_name=role_name,
            timeout=timeout,
            write_access_buckets=write_access_buckets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="diskSpaceUsedMbMetric")
    def disk_space_used_mb_metric(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "diskSpaceUsedMbMetric", [props]))

    @jsii.member(jsii_name="elapsedTimeMetric")
    def elapsed_time_metric(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "elapsedTimeMetric", [props]))

    @jsii.member(jsii_name="jvmHeapUsageMetric")
    def jvm_heap_usage_metric(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "jvmHeapUsageMetric", [props]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        dimension_type: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param dimension_type: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            def stub(
                metric_name: builtins.str,
                dimension_type: builtins.str,
                *,
                account: typing.Optional[builtins.str] = None,
                color: typing.Optional[builtins.str] = None,
                dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                label: typing.Optional[builtins.str] = None,
                period: typing.Optional[aws_cdk.Duration] = None,
                region: typing.Optional[builtins.str] = None,
                statistic: typing.Optional[builtins.str] = None,
                unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, dimension_type, props]))

    @jsii.member(jsii_name="metricAllExecutionAttemptsFailed")
    def metric_all_execution_attempts_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricAllExecutionAttemptsFailed", [props]))

    @jsii.member(jsii_name="metricFailure")
    def metric_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricFailure", [props]))

    @jsii.member(jsii_name="metricSuccess")
    def metric_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSuccess", [props]))

    @jsii.member(jsii_name="metricTimeout")
    def metric_timeout(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricTimeout", [props]))

    @jsii.member(jsii_name="runTimeInMiliseconds")
    def run_time_in_miliseconds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "runTimeInMiliseconds", [props]))

    @builtins.property
    @jsii.member(jsii_name="allExecutionAttemptsFailedEventDetailType")
    def all_execution_attempts_failed_event_detail_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allExecutionAttemptsFailedEventDetailType"))

    @builtins.property
    @jsii.member(jsii_name="allExecutionAttemptsFailedEventSource")
    def all_execution_attempts_failed_event_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allExecutionAttemptsFailedEventSource"))

    @builtins.property
    @jsii.member(jsii_name="executionFailureRule")
    def execution_failure_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "executionFailureRule"))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> aws_cdk.aws_glue.CfnJob:
        return typing.cast(aws_cdk.aws_glue.CfnJob, jsii.get(self, "job"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.SingletonFunction:
        return typing.cast(aws_cdk.aws_lambda.SingletonFunction, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="metricFailureRule")
    def metric_failure_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "metricFailureRule"))

    @builtins.property
    @jsii.member(jsii_name="metricSuccessRule")
    def metric_success_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "metricSuccessRule"))

    @builtins.property
    @jsii.member(jsii_name="metricTimeoutRule")
    def metric_timeout_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "metricTimeoutRule"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


class GlueJobOps(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.GlueJobOps",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: "IGlueOpsProperties",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                props: "IGlueOpsProperties",
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarmsSev2")
    def alarms_sev2(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return typing.cast(typing.List[aws_cdk.aws_cloudwatch.Alarm], jsii.get(self, "alarmsSev2"))

    @builtins.property
    @jsii.member(jsii_name="alarmsSev3")
    def alarms_sev3(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return typing.cast(typing.List[aws_cdk.aws_cloudwatch.Alarm], jsii.get(self, "alarmsSev3"))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> GlueJob:
        return typing.cast(GlueJob, jsii.get(self, "job"))

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding80PercentAlarm")
    def jvm_heap_size_exceeding80_percent_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "jvmHeapSizeExceeding80PercentAlarm"))

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding90PercentAlarm")
    def jvm_heap_size_exceeding90_percent_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "jvmHeapSizeExceeding90PercentAlarm"))

    @builtins.property
    @jsii.member(jsii_name="metricAllExecutionAttemptsFailedAlarm")
    def metric_all_execution_attempts_failed_alarm(
        self,
    ) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "metricAllExecutionAttemptsFailedAlarm"))

    @builtins.property
    @jsii.member(jsii_name="metricExecutionFailureAlarm")
    def metric_execution_failure_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "metricExecutionFailureAlarm"))

    @builtins.property
    @jsii.member(jsii_name="dashboard")
    def dashboard(self) -> aws_cdk.aws_cloudwatch.Dashboard:
        return typing.cast(aws_cdk.aws_cloudwatch.Dashboard, jsii.get(self, "dashboard"))

    @dashboard.setter
    def dashboard(self, value: aws_cdk.aws_cloudwatch.Dashboard) -> None:
        if __debug__:
            def stub(value: aws_cdk.aws_cloudwatch.Dashboard) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboard", value)


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.GlueJobProperties",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_bucket": "deploymentBucket",
        "job_script": "jobScript",
        "job_type": "jobType",
        "name": "name",
        "worker_type": "workerType",
        "description": "description",
        "glue_version": "glueVersion",
        "job_args": "jobArgs",
        "max_capacity": "maxCapacity",
        "max_concurrent_runs": "maxConcurrentRuns",
        "max_retries": "maxRetries",
        "number_of_workers": "numberOfWorkers",
        "read_access_buckets": "readAccessBuckets",
        "role_name": "roleName",
        "timeout": "timeout",
        "write_access_buckets": "writeAccessBuckets",
    },
)
class GlueJobProperties:
    def __init__(
        self,
        *,
        deployment_bucket: aws_cdk.aws_s3.IBucket,
        job_script: builtins.str,
        job_type: "GlueJobType",
        name: builtins.str,
        worker_type: "GlueWorkerType",
        description: typing.Optional[builtins.str] = None,
        glue_version: typing.Optional["GlueVersion"] = None,
        job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        role_name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
    ) -> None:
        '''
        :param deployment_bucket: 
        :param job_script: 
        :param job_type: 
        :param name: 
        :param worker_type: 
        :param description: 
        :param glue_version: 
        :param job_args: 
        :param max_capacity: 
        :param max_concurrent_runs: 
        :param max_retries: 
        :param number_of_workers: 
        :param read_access_buckets: 
        :param role_name: 
        :param timeout: 
        :param write_access_buckets: 
        '''
        if __debug__:
            def stub(
                *,
                deployment_bucket: aws_cdk.aws_s3.IBucket,
                job_script: builtins.str,
                job_type: "GlueJobType",
                name: builtins.str,
                worker_type: "GlueWorkerType",
                description: typing.Optional[builtins.str] = None,
                glue_version: typing.Optional["GlueVersion"] = None,
                job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                max_capacity: typing.Optional[jsii.Number] = None,
                max_concurrent_runs: typing.Optional[jsii.Number] = None,
                max_retries: typing.Optional[jsii.Number] = None,
                number_of_workers: typing.Optional[jsii.Number] = None,
                read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
                role_name: typing.Optional[builtins.str] = None,
                timeout: typing.Optional[jsii.Number] = None,
                write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument deployment_bucket", value=deployment_bucket, expected_type=type_hints["deployment_bucket"])
            check_type(argname="argument job_script", value=job_script, expected_type=type_hints["job_script"])
            check_type(argname="argument job_type", value=job_type, expected_type=type_hints["job_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument job_args", value=job_args, expected_type=type_hints["job_args"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument read_access_buckets", value=read_access_buckets, expected_type=type_hints["read_access_buckets"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument write_access_buckets", value=write_access_buckets, expected_type=type_hints["write_access_buckets"])
        self._values: typing.Dict[str, typing.Any] = {
            "deployment_bucket": deployment_bucket,
            "job_script": job_script,
            "job_type": job_type,
            "name": name,
            "worker_type": worker_type,
        }
        if description is not None:
            self._values["description"] = description
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if job_args is not None:
            self._values["job_args"] = job_args
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if read_access_buckets is not None:
            self._values["read_access_buckets"] = read_access_buckets
        if role_name is not None:
            self._values["role_name"] = role_name
        if timeout is not None:
            self._values["timeout"] = timeout
        if write_access_buckets is not None:
            self._values["write_access_buckets"] = write_access_buckets

    @builtins.property
    def deployment_bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("deployment_bucket")
        assert result is not None, "Required property 'deployment_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def job_script(self) -> builtins.str:
        result = self._values.get("job_script")
        assert result is not None, "Required property 'job_script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_type(self) -> "GlueJobType":
        result = self._values.get("job_type")
        assert result is not None, "Required property 'job_type' is missing"
        return typing.cast("GlueJobType", result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def worker_type(self) -> "GlueWorkerType":
        result = self._values.get("worker_type")
        assert result is not None, "Required property 'worker_type' is missing"
        return typing.cast("GlueWorkerType", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glue_version(self) -> typing.Optional["GlueVersion"]:
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional["GlueVersion"], result)

    @builtins.property
    def job_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("job_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("read_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("write_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueJobProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.GlueJobType")
class GlueJobType(enum.Enum):
    GLUE_ETL = "GLUE_ETL"
    GLUE_STREAMING = "GLUE_STREAMING"


class GlueTable(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.GlueTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: "IGlueTableProperties",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                props: "IGlueTableProperties",
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_glue.CfnTable:
        return typing.cast(aws_cdk.aws_glue.CfnTable, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.GlueVersion")
class GlueVersion(enum.Enum):
    V_0 = "V_0"
    V_1 = "V_1"
    V_2 = "V_2"
    V_3 = "V_3"


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.GlueWorkerType")
class GlueWorkerType(enum.Enum):
    STANDARD = "STANDARD"
    G1_X = "G1_X"
    G2_X = "G2_X"


@jsii.interface(
    jsii_type="@randyridgley/cdk-datalake-constructs.IGlueCrawlerProperties"
)
class IGlueCrawlerProperties(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        ...

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        ...

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lfS3Resource")
    def lf_s3_resource(self) -> aws_cdk.CfnResource:
        ...

    @lf_s3_resource.setter
    def lf_s3_resource(self, value: aws_cdk.CfnResource) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        ...

    @bucket_prefix.setter
    def bucket_prefix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> typing.Optional[builtins.str]:
        ...

    @role_name.setter
    def role_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> typing.Optional[aws_cdk.aws_glue.CfnTrigger]:
        ...

    @trigger.setter
    def trigger(self, value: typing.Optional[aws_cdk.aws_glue.CfnTrigger]) -> None:
        ...


class _IGlueCrawlerPropertiesProxy:
    __jsii_type__: typing.ClassVar[str] = "@randyridgley/cdk-datalake-constructs.IGlueCrawlerProperties"

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="lfS3Resource")
    def lf_s3_resource(self) -> aws_cdk.CfnResource:
        return typing.cast(aws_cdk.CfnResource, jsii.get(self, "lfS3Resource"))

    @lf_s3_resource.setter
    def lf_s3_resource(self, value: aws_cdk.CfnResource) -> None:
        if __debug__:
            def stub(value: aws_cdk.CfnResource) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lfS3Resource", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Optional[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Optional[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value)

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> typing.Optional[aws_cdk.aws_glue.CfnTrigger]:
        return typing.cast(typing.Optional[aws_cdk.aws_glue.CfnTrigger], jsii.get(self, "trigger"))

    @trigger.setter
    def trigger(self, value: typing.Optional[aws_cdk.aws_glue.CfnTrigger]) -> None:
        if __debug__:
            def stub(value: typing.Optional[aws_cdk.aws_glue.CfnTrigger]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trigger", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGlueCrawlerProperties).__jsii_proxy_class__ = lambda : _IGlueCrawlerPropertiesProxy


@jsii.interface(jsii_type="@randyridgley/cdk-datalake-constructs.IGlueOpsProperties")
class IGlueOpsProperties(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> GlueJob:
        ...

    @job.setter
    def job(self, value: GlueJob) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding80percent")
    def jvm_heap_size_exceeding80percent(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @jvm_heap_size_exceeding80percent.setter
    def jvm_heap_size_exceeding80percent(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding90percent")
    def jvm_heap_size_exceeding90percent(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @jvm_heap_size_exceeding90percent.setter
    def jvm_heap_size_exceeding90percent(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="metricAllExecutionAttemptsFailed")
    def metric_all_execution_attempts_failed(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @metric_all_execution_attempts_failed.setter
    def metric_all_execution_attempts_failed(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="metricExecutionFailure")
    def metric_execution_failure(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @metric_execution_failure.setter
    def metric_execution_failure(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...


class _IGlueOpsPropertiesProxy:
    __jsii_type__: typing.ClassVar[str] = "@randyridgley/cdk-datalake-constructs.IGlueOpsProperties"

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> GlueJob:
        return typing.cast(GlueJob, jsii.get(self, "job"))

    @job.setter
    def job(self, value: GlueJob) -> None:
        if __debug__:
            def stub(value: GlueJob) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "job", value)

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding80percent")
    def jvm_heap_size_exceeding80percent(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "jvmHeapSizeExceeding80percent"))

    @jvm_heap_size_exceeding80percent.setter
    def jvm_heap_size_exceeding80percent(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jvmHeapSizeExceeding80percent", value)

    @builtins.property
    @jsii.member(jsii_name="jvmHeapSizeExceeding90percent")
    def jvm_heap_size_exceeding90percent(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "jvmHeapSizeExceeding90percent"))

    @jvm_heap_size_exceeding90percent.setter
    def jvm_heap_size_exceeding90percent(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jvmHeapSizeExceeding90percent", value)

    @builtins.property
    @jsii.member(jsii_name="metricAllExecutionAttemptsFailed")
    def metric_all_execution_attempts_failed(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "metricAllExecutionAttemptsFailed"))

    @metric_all_execution_attempts_failed.setter
    def metric_all_execution_attempts_failed(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricAllExecutionAttemptsFailed", value)

    @builtins.property
    @jsii.member(jsii_name="metricExecutionFailure")
    def metric_execution_failure(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "metricExecutionFailure"))

    @metric_execution_failure.setter
    def metric_execution_failure(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricExecutionFailure", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGlueOpsProperties).__jsii_proxy_class__ = lambda : _IGlueOpsPropertiesProxy


@jsii.interface(jsii_type="@randyridgley/cdk-datalake-constructs.IGlueTableProperties")
class IGlueTableProperties(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        ...

    @catalog_id.setter
    def catalog_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        ...

    @columns.setter
    def columns(
        self,
        value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        ...

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        ...

    @description.setter
    def description(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> builtins.str:
        ...

    @input_format.setter
    def input_format(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        ...

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        ...

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="partitionKeys")
    def partition_keys(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        ...

    @partition_keys.setter
    def partition_keys(
        self,
        value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> builtins.str:
        ...

    @s3_location.setter
    def s3_location(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="serdeParameters")
    def serde_parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        ...

    @serde_parameters.setter
    def serde_parameters(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="serializationLibrary")
    def serialization_library(self) -> builtins.str:
        ...

    @serialization_library.setter
    def serialization_library(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        ...

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        ...


class _IGlueTablePropertiesProxy:
    __jsii_type__: typing.ClassVar[str] = "@randyridgley/cdk-datalake-constructs.IGlueTableProperties"

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @catalog_id.setter
    def catalog_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogId", value)

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        return typing.cast(typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]], jsii.get(self, "columns"))

    @columns.setter
    def columns(
        self,
        value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputFormat"))

    @input_format.setter
    def input_format(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputFormat", value)

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="partitionKeys")
    def partition_keys(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        return typing.cast(typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]], jsii.get(self, "partitionKeys"))

    @partition_keys.setter
    def partition_keys(
        self,
        value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeys", value)

    @builtins.property
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Location"))

    @s3_location.setter
    def s3_location(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Location", value)

    @builtins.property
    @jsii.member(jsii_name="serdeParameters")
    def serde_parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "serdeParameters"))

    @serde_parameters.setter
    def serde_parameters(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serdeParameters", value)

    @builtins.property
    @jsii.member(jsii_name="serializationLibrary")
    def serialization_library(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serializationLibrary"))

    @serialization_library.setter
    def serialization_library(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serializationLibrary", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGlueTableProperties).__jsii_proxy_class__ = lambda : _IGlueTablePropertiesProxy


@jsii.interface(
    jsii_type="@randyridgley/cdk-datalake-constructs.IKinesisOpsProperties"
)
class IKinesisOpsProperties(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="deliveryStream")
    def delivery_stream(self) -> "S3DeliveryStream":
        ...

    @delivery_stream.setter
    def delivery_stream(self, value: "S3DeliveryStream") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> "KinesisStream":
        ...

    @stream.setter
    def stream(self, value: "KinesisStream") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3Critical")
    def firehose_delivery_to_s3_critical(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @firehose_delivery_to_s3_critical.setter
    def firehose_delivery_to_s3_critical(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3Warning")
    def firehose_delivery_to_s3_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @firehose_delivery_to_s3_warning.setter
    def firehose_delivery_to_s3_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamGetRecordsWarning")
    def input_stream_get_records_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_get_records_warning.setter
    def input_stream_get_records_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeCritical")
    def input_stream_iterator_age_critical(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_iterator_age_critical.setter
    def input_stream_iterator_age_critical(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeWarning")
    def input_stream_iterator_age_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_iterator_age_warning.setter
    def input_stream_iterator_age_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamPutRecordsWarning")
    def input_stream_put_records_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_put_records_warning.setter
    def input_stream_put_records_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamReadThroughputWarning")
    def input_stream_read_throughput_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_read_throughput_warning.setter
    def input_stream_read_throughput_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputStreamWriteThroughputWarning")
    def input_stream_write_throughput_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        ...

    @input_stream_write_throughput_warning.setter
    def input_stream_write_throughput_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        ...


class _IKinesisOpsPropertiesProxy:
    __jsii_type__: typing.ClassVar[str] = "@randyridgley/cdk-datalake-constructs.IKinesisOpsProperties"

    @builtins.property
    @jsii.member(jsii_name="deliveryStream")
    def delivery_stream(self) -> "S3DeliveryStream":
        return typing.cast("S3DeliveryStream", jsii.get(self, "deliveryStream"))

    @delivery_stream.setter
    def delivery_stream(self, value: "S3DeliveryStream") -> None:
        if __debug__:
            def stub(value: "S3DeliveryStream") -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStream", value)

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> "KinesisStream":
        return typing.cast("KinesisStream", jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: "KinesisStream") -> None:
        if __debug__:
            def stub(value: "KinesisStream") -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value)

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3Critical")
    def firehose_delivery_to_s3_critical(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "firehoseDeliveryToS3Critical"))

    @firehose_delivery_to_s3_critical.setter
    def firehose_delivery_to_s3_critical(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseDeliveryToS3Critical", value)

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3Warning")
    def firehose_delivery_to_s3_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "firehoseDeliveryToS3Warning"))

    @firehose_delivery_to_s3_warning.setter
    def firehose_delivery_to_s3_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firehoseDeliveryToS3Warning", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamGetRecordsWarning")
    def input_stream_get_records_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamGetRecordsWarning"))

    @input_stream_get_records_warning.setter
    def input_stream_get_records_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamGetRecordsWarning", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeCritical")
    def input_stream_iterator_age_critical(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamIteratorAgeCritical"))

    @input_stream_iterator_age_critical.setter
    def input_stream_iterator_age_critical(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamIteratorAgeCritical", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeWarning")
    def input_stream_iterator_age_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamIteratorAgeWarning"))

    @input_stream_iterator_age_warning.setter
    def input_stream_iterator_age_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamIteratorAgeWarning", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamPutRecordsWarning")
    def input_stream_put_records_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamPutRecordsWarning"))

    @input_stream_put_records_warning.setter
    def input_stream_put_records_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamPutRecordsWarning", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamReadThroughputWarning")
    def input_stream_read_throughput_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamReadThroughputWarning"))

    @input_stream_read_throughput_warning.setter
    def input_stream_read_throughput_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamReadThroughputWarning", value)

    @builtins.property
    @jsii.member(jsii_name="inputStreamWriteThroughputWarning")
    def input_stream_write_throughput_warning(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions]:
        return typing.cast(typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions], jsii.get(self, "inputStreamWriteThroughputWarning"))

    @input_stream_write_throughput_warning.setter
    def input_stream_write_throughput_warning(
        self,
        value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[aws_cdk.aws_cloudwatch.CreateAlarmOptions],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStreamWriteThroughputWarning", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKinesisOpsProperties).__jsii_proxy_class__ = lambda : _IKinesisOpsPropertiesProxy


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.JDBCProperties",
    jsii_struct_bases=[],
    name_mapping={"jdbc": "jdbc", "password": "password", "username": "username"},
)
class JDBCProperties:
    def __init__(
        self,
        *,
        jdbc: builtins.str,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param jdbc: 
        :param password: 
        :param username: 
        '''
        if __debug__:
            def stub(
                *,
                jdbc: builtins.str,
                password: builtins.str,
                username: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument jdbc", value=jdbc, expected_type=type_hints["jdbc"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "jdbc": jdbc,
            "password": password,
            "username": username,
        }

    @builtins.property
    def jdbc(self) -> builtins.str:
        result = self._values.get("jdbc")
        assert result is not None, "Required property 'jdbc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JDBCProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.JobProperties",
    jsii_struct_bases=[],
    name_mapping={
        "job_script": "jobScript",
        "job_type": "jobType",
        "name": "name",
        "worker_type": "workerType",
        "description": "description",
        "destination_location": "destinationLocation",
        "glue_version": "glueVersion",
        "job_args": "jobArgs",
        "max_capacity": "maxCapacity",
        "max_concurrent_runs": "maxConcurrentRuns",
        "max_retries": "maxRetries",
        "number_of_workers": "numberOfWorkers",
        "read_access_buckets": "readAccessBuckets",
        "role_name": "roleName",
        "timeout": "timeout",
        "write_access_buckets": "writeAccessBuckets",
    },
)
class JobProperties:
    def __init__(
        self,
        *,
        job_script: builtins.str,
        job_type: GlueJobType,
        name: builtins.str,
        worker_type: GlueWorkerType,
        description: typing.Optional[builtins.str] = None,
        destination_location: typing.Optional[DataTier] = None,
        glue_version: typing.Optional[GlueVersion] = None,
        job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        role_name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
    ) -> None:
        '''
        :param job_script: 
        :param job_type: 
        :param name: 
        :param worker_type: 
        :param description: 
        :param destination_location: 
        :param glue_version: 
        :param job_args: 
        :param max_capacity: 
        :param max_concurrent_runs: 
        :param max_retries: 
        :param number_of_workers: 
        :param read_access_buckets: 
        :param role_name: 
        :param timeout: 
        :param write_access_buckets: 
        '''
        if __debug__:
            def stub(
                *,
                job_script: builtins.str,
                job_type: GlueJobType,
                name: builtins.str,
                worker_type: GlueWorkerType,
                description: typing.Optional[builtins.str] = None,
                destination_location: typing.Optional[DataTier] = None,
                glue_version: typing.Optional[GlueVersion] = None,
                job_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                max_capacity: typing.Optional[jsii.Number] = None,
                max_concurrent_runs: typing.Optional[jsii.Number] = None,
                max_retries: typing.Optional[jsii.Number] = None,
                number_of_workers: typing.Optional[jsii.Number] = None,
                read_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
                role_name: typing.Optional[builtins.str] = None,
                timeout: typing.Optional[jsii.Number] = None,
                write_access_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument job_script", value=job_script, expected_type=type_hints["job_script"])
            check_type(argname="argument job_type", value=job_type, expected_type=type_hints["job_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_location", value=destination_location, expected_type=type_hints["destination_location"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument job_args", value=job_args, expected_type=type_hints["job_args"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument read_access_buckets", value=read_access_buckets, expected_type=type_hints["read_access_buckets"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument write_access_buckets", value=write_access_buckets, expected_type=type_hints["write_access_buckets"])
        self._values: typing.Dict[str, typing.Any] = {
            "job_script": job_script,
            "job_type": job_type,
            "name": name,
            "worker_type": worker_type,
        }
        if description is not None:
            self._values["description"] = description
        if destination_location is not None:
            self._values["destination_location"] = destination_location
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if job_args is not None:
            self._values["job_args"] = job_args
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if read_access_buckets is not None:
            self._values["read_access_buckets"] = read_access_buckets
        if role_name is not None:
            self._values["role_name"] = role_name
        if timeout is not None:
            self._values["timeout"] = timeout
        if write_access_buckets is not None:
            self._values["write_access_buckets"] = write_access_buckets

    @builtins.property
    def job_script(self) -> builtins.str:
        result = self._values.get("job_script")
        assert result is not None, "Required property 'job_script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_type(self) -> GlueJobType:
        result = self._values.get("job_type")
        assert result is not None, "Required property 'job_type' is missing"
        return typing.cast(GlueJobType, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def worker_type(self) -> GlueWorkerType:
        result = self._values.get("worker_type")
        assert result is not None, "Required property 'worker_type' is missing"
        return typing.cast(GlueWorkerType, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_location(self) -> typing.Optional[DataTier]:
        result = self._values.get("destination_location")
        return typing.cast(typing.Optional[DataTier], result)

    @builtins.property
    def glue_version(self) -> typing.Optional[GlueVersion]:
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional[GlueVersion], result)

    @builtins.property
    def job_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("job_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("read_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_access_buckets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        result = self._values.get("write_access_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisOps(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.KinesisOps",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IKinesisOpsProperties,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                props: IKinesisOpsProperties,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarmsSev2")
    def alarms_sev2(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return typing.cast(typing.List[aws_cdk.aws_cloudwatch.Alarm], jsii.get(self, "alarmsSev2"))

    @builtins.property
    @jsii.member(jsii_name="alarmsSev3")
    def alarms_sev3(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return typing.cast(typing.List[aws_cdk.aws_cloudwatch.Alarm], jsii.get(self, "alarmsSev3"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStream")
    def delivery_stream(self) -> "S3DeliveryStream":
        return typing.cast("S3DeliveryStream", jsii.get(self, "deliveryStream"))

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3CriticalAlarm")
    def firehose_delivery_to_s3_critical_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "firehoseDeliveryToS3CriticalAlarm"))

    @builtins.property
    @jsii.member(jsii_name="firehoseDeliveryToS3WarningAlarm")
    def firehose_delivery_to_s3_warning_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "firehoseDeliveryToS3WarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamGetRecordsWarningAlarm")
    def input_stream_get_records_warning_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamGetRecordsWarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeCriticalAlarm")
    def input_stream_iterator_age_critical_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamIteratorAgeCriticalAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamIteratorAgeWarningAlarm")
    def input_stream_iterator_age_warning_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamIteratorAgeWarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamPutRecordsWarningAlarm")
    def input_stream_put_records_warning_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamPutRecordsWarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamReadThroughputWarningAlarm")
    def input_stream_read_throughput_warning_alarm(
        self,
    ) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamReadThroughputWarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="inputStreamWriteThroughputWarningAlarm")
    def input_stream_write_throughput_warning_alarm(
        self,
    ) -> aws_cdk.aws_cloudwatch.Alarm:
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "inputStreamWriteThroughputWarningAlarm"))

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> "KinesisStream":
        return typing.cast("KinesisStream", jsii.get(self, "stream"))

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @builtins.property
    @jsii.member(jsii_name="dashboard")
    def dashboard(self) -> aws_cdk.aws_cloudwatch.Dashboard:
        return typing.cast(aws_cdk.aws_cloudwatch.Dashboard, jsii.get(self, "dashboard"))

    @dashboard.setter
    def dashboard(self, value: aws_cdk.aws_cloudwatch.Dashboard) -> None:
        if __debug__:
            def stub(value: aws_cdk.aws_cloudwatch.Dashboard) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboard", value)


class KinesisStream(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.KinesisStream",
):
    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        encryption: typing.Optional[aws_cdk.aws_kinesis.StreamEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        retention_period: typing.Optional[aws_cdk.Duration] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_mode: typing.Optional[aws_cdk.aws_kinesis.StreamMode] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param encryption: The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - StreamEncryption.KMS if encrypted Streams are supported in the region or StreamEncryption.UNENCRYPTED otherwise. StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        :param encryption_key: External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: - Kinesis Data Streams master key ('/alias/aws/kinesis'). If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key will be created and associated with this stream.
        :param retention_period: The number of hours for the data records that are stored in shards to remain accessible. Default: Duration.hours(24)
        :param shard_count: The number of shards for the stream. Can only be provided if streamMode is Provisioned. Default: 1
        :param stream_mode: The capacity mode of this stream. Default: StreamMode.PROVISIONED
        :param stream_name: Enforces a particular physical stream name. Default: 
        '''
        if __debug__:
            def stub(
                parent: constructs.Construct,
                name: builtins.str,
                *,
                encryption: typing.Optional[aws_cdk.aws_kinesis.StreamEncryption] = None,
                encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
                retention_period: typing.Optional[aws_cdk.Duration] = None,
                shard_count: typing.Optional[jsii.Number] = None,
                stream_mode: typing.Optional[aws_cdk.aws_kinesis.StreamMode] = None,
                stream_name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = aws_cdk.aws_kinesis.StreamProps(
            encryption=encryption,
            encryption_key=encryption_key,
            retention_period=retention_period,
            shard_count=shard_count,
            stream_mode=stream_mode,
            stream_name=stream_name,
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            def stub(
                metric_name: builtins.str,
                *,
                account: typing.Optional[builtins.str] = None,
                color: typing.Optional[builtins.str] = None,
                dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                label: typing.Optional[builtins.str] = None,
                period: typing.Optional[aws_cdk.Duration] = None,
                region: typing.Optional[builtins.str] = None,
                statistic: typing.Optional[builtins.str] = None,
                unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricGetRecordsBytes")
    def metric_get_records_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricGetRecordsBytes", [props]))

    @jsii.member(jsii_name="metricGetRecordsIteratorAgeMilliseconds")
    def metric_get_records_iterator_age_milliseconds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricGetRecordsIteratorAgeMilliseconds", [props]))

    @jsii.member(jsii_name="metricGetRecordsLatency")
    def metric_get_records_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricGetRecordsLatency", [props]))

    @jsii.member(jsii_name="metricGetRecordsRecords")
    def metric_get_records_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricGetRecordsRecords", [props]))

    @jsii.member(jsii_name="metricGetRecordsSuccess")
    def metric_get_records_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricGetRecordsSuccess", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

    @jsii.member(jsii_name="metricPutRecordBytes")
    def metric_put_record_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordBytes", [props]))

    @jsii.member(jsii_name="metricPutRecordLatency")
    def metric_put_record_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordLatency", [props]))

    @jsii.member(jsii_name="metricPutRecordsBytes")
    def metric_put_records_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordsBytes", [props]))

    @jsii.member(jsii_name="metricPutRecordsLatency")
    def metric_put_records_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordsLatency", [props]))

    @jsii.member(jsii_name="metricPutRecordsRecords")
    def metric_put_records_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordsRecords", [props]))

    @jsii.member(jsii_name="metricPutRecordsSuccess")
    def metric_put_records_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordsSuccess", [props]))

    @jsii.member(jsii_name="metricPutRecordSuccess")
    def metric_put_record_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricPutRecordSuccess", [props]))

    @jsii.member(jsii_name="metricReadProvisionedThroughputExceeded")
    def metric_read_provisioned_throughput_exceeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricReadProvisionedThroughputExceeded", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardEventBytes")
    def metric_subscribe_to_shard_event_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardEventBytes", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardEventMillisBehindLatest")
    def metric_subscribe_to_shard_event_millis_behind_latest(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardEventMillisBehindLatest", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardEventRecords")
    def metric_subscribe_to_shard_event_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardEventRecords", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardEventSuccess")
    def metric_subscribe_to_shard_event_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardEventSuccess", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardRateExceeded")
    def metric_subscribe_to_shard_rate_exceeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardRateExceeded", [props]))

    @jsii.member(jsii_name="metricSubscribeToShardSuccess")
    def metric_subscribe_to_shard_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricSubscribeToShardSuccess", [props]))

    @jsii.member(jsii_name="metricWriteProvisionedThroughputExceeded")
    def metric_write_provisioned_throughput_exceeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricWriteProvisionedThroughputExceeded", [props]))

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> aws_cdk.aws_kinesis.Stream:
        return typing.cast(aws_cdk.aws_kinesis.Stream, jsii.get(self, "stream"))


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.LakeKind")
class LakeKind(enum.Enum):
    DATA_PRODUCT = "DATA_PRODUCT"
    CENTRAL_CATALOG = "CENTRAL_CATALOG"
    CONSUMER = "CONSUMER"
    DATA_PRODUCT_AND_CATALOG = "DATA_PRODUCT_AND_CATALOG"


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.LambdaDataGeneratorProperties",
    jsii_struct_bases=[],
    name_mapping={
        "code": "code",
        "function_name": "functionName",
        "handler": "handler",
        "rule_name": "ruleName",
        "runtime": "runtime",
        "schedule": "schedule",
        "timeout": "timeout",
    },
)
class LambdaDataGeneratorProperties:
    def __init__(
        self,
        *,
        code: aws_cdk.aws_lambda.Code,
        function_name: builtins.str,
        handler: builtins.str,
        rule_name: builtins.str,
        runtime: aws_cdk.aws_lambda.Runtime,
        schedule: aws_cdk.aws_events.Schedule,
        timeout: aws_cdk.Duration,
    ) -> None:
        '''
        :param code: 
        :param function_name: 
        :param handler: 
        :param rule_name: 
        :param runtime: 
        :param schedule: 
        :param timeout: 
        '''
        if __debug__:
            def stub(
                *,
                code: aws_cdk.aws_lambda.Code,
                function_name: builtins.str,
                handler: builtins.str,
                rule_name: builtins.str,
                runtime: aws_cdk.aws_lambda.Runtime,
                schedule: aws_cdk.aws_events.Schedule,
                timeout: aws_cdk.Duration,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {
            "code": code,
            "function_name": function_name,
            "handler": handler,
            "rule_name": rule_name,
            "runtime": runtime,
            "schedule": schedule,
            "timeout": timeout,
        }

    @builtins.property
    def code(self) -> aws_cdk.aws_lambda.Code:
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(aws_cdk.aws_lambda.Code, result)

    @builtins.property
    def function_name(self) -> builtins.str:
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> builtins.str:
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> aws_cdk.aws_lambda.Runtime:
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(aws_cdk.aws_lambda.Runtime, result)

    @builtins.property
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(aws_cdk.aws_events.Schedule, result)

    @builtins.property
    def timeout(self) -> aws_cdk.Duration:
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(aws_cdk.Duration, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDataGeneratorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.NameBuilderParameters",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "account_id": "accountId",
        "region": "region",
        "resource_use": "resourceUse",
        "stage": "stage",
    },
)
class NameBuilderParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource_use: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param account_id: 
        :param region: 
        :param resource_use: 
        :param stage: 
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                account_id: typing.Optional[builtins.str] = None,
                region: typing.Optional[builtins.str] = None,
                resource_use: typing.Optional[builtins.str] = None,
                stage: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_use", value=resource_use, expected_type=type_hints["resource_use"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if account_id is not None:
            self._values["account_id"] = account_id
        if region is not None:
            self._values["region"] = region
        if resource_use is not None:
            self._values["resource_use"] = resource_use
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_use(self) -> typing.Optional[builtins.str]:
        result = self._values.get("resource_use")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameBuilderParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.Permissions")
class Permissions(enum.Enum):
    ALTER = "ALTER"
    CREATE_DATABASE = "CREATE_DATABASE"
    CREATE_TABLE = "CREATE_TABLE"
    DATA_LOCATION_ACCESS = "DATA_LOCATION_ACCESS"
    DELETE = "DELETE"
    DESCRIBE = "DESCRIBE"
    DROP = "DROP"
    INSERT = "INSERT"
    SELECT = "SELECT"
    ASSOCIATE = "ASSOCIATE"
    CREATE_TABLE_READ_WRITE = "CREATE_TABLE_READ_WRITE"


class Pipeline(
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.Pipeline",
):
    def __init__(
        self,
        *,
        data_drop_tier: DataTier,
        destination_prefix: builtins.str,
        name: builtins.str,
        type: DataPipelineType,
        jdbc_properties: typing.Optional[typing.Union[JDBCProperties, typing.Dict[str, typing.Any]]] = None,
        job: typing.Optional[typing.Union[JobProperties, typing.Dict[str, typing.Any]]] = None,
        s3_properties: typing.Optional[typing.Union["S3Properties", typing.Dict[str, typing.Any]]] = None,
        stream_properties: typing.Optional[typing.Union["StreamProperties", typing.Dict[str, typing.Any]]] = None,
        table: typing.Optional[typing.Union["TableProps", typing.Dict[str, typing.Any]]] = None,
        tiers: typing.Optional[typing.Sequence[DataTier]] = None,
    ) -> None:
        '''
        :param data_drop_tier: 
        :param destination_prefix: 
        :param name: 
        :param type: 
        :param jdbc_properties: 
        :param job: 
        :param s3_properties: 
        :param stream_properties: 
        :param table: 
        :param tiers: 
        '''
        props = PipelineProperties(
            data_drop_tier=data_drop_tier,
            destination_prefix=destination_prefix,
            name=name,
            type=type,
            jdbc_properties=jdbc_properties,
            job=job,
            s3_properties=s3_properties,
            stream_properties=stream_properties,
            table=table,
            tiers=tiers,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="dataSetDropTier")
    def data_set_drop_tier(self) -> DataTier:
        return typing.cast(DataTier, jsii.get(self, "dataSetDropTier"))

    @builtins.property
    @jsii.member(jsii_name="destinationPrefix")
    def destination_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPrefix"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="tiers")
    def tiers(self) -> typing.List[DataTier]:
        return typing.cast(typing.List[DataTier], jsii.get(self, "tiers"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> DataPipelineType:
        return typing.cast(DataPipelineType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="jdbcProperties")
    def jdbc_properties(self) -> typing.Optional[JDBCProperties]:
        return typing.cast(typing.Optional[JDBCProperties], jsii.get(self, "jdbcProperties"))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> typing.Optional[JobProperties]:
        return typing.cast(typing.Optional[JobProperties], jsii.get(self, "job"))

    @builtins.property
    @jsii.member(jsii_name="s3Properties")
    def s3_properties(self) -> typing.Optional["S3Properties"]:
        return typing.cast(typing.Optional["S3Properties"], jsii.get(self, "s3Properties"))

    @builtins.property
    @jsii.member(jsii_name="streamProperties")
    def stream_properties(self) -> typing.Optional["StreamProperties"]:
        return typing.cast(typing.Optional["StreamProperties"], jsii.get(self, "streamProperties"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> typing.Optional["TableProps"]:
        return typing.cast(typing.Optional["TableProps"], jsii.get(self, "table"))


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.PipelineProperties",
    jsii_struct_bases=[],
    name_mapping={
        "data_drop_tier": "dataDropTier",
        "destination_prefix": "destinationPrefix",
        "name": "name",
        "type": "type",
        "jdbc_properties": "jdbcProperties",
        "job": "job",
        "s3_properties": "s3Properties",
        "stream_properties": "streamProperties",
        "table": "table",
        "tiers": "tiers",
    },
)
class PipelineProperties:
    def __init__(
        self,
        *,
        data_drop_tier: DataTier,
        destination_prefix: builtins.str,
        name: builtins.str,
        type: DataPipelineType,
        jdbc_properties: typing.Optional[typing.Union[JDBCProperties, typing.Dict[str, typing.Any]]] = None,
        job: typing.Optional[typing.Union[JobProperties, typing.Dict[str, typing.Any]]] = None,
        s3_properties: typing.Optional[typing.Union["S3Properties", typing.Dict[str, typing.Any]]] = None,
        stream_properties: typing.Optional[typing.Union["StreamProperties", typing.Dict[str, typing.Any]]] = None,
        table: typing.Optional[typing.Union["TableProps", typing.Dict[str, typing.Any]]] = None,
        tiers: typing.Optional[typing.Sequence[DataTier]] = None,
    ) -> None:
        '''
        :param data_drop_tier: 
        :param destination_prefix: 
        :param name: 
        :param type: 
        :param jdbc_properties: 
        :param job: 
        :param s3_properties: 
        :param stream_properties: 
        :param table: 
        :param tiers: 
        '''
        if isinstance(jdbc_properties, dict):
            jdbc_properties = JDBCProperties(**jdbc_properties)
        if isinstance(job, dict):
            job = JobProperties(**job)
        if isinstance(s3_properties, dict):
            s3_properties = S3Properties(**s3_properties)
        if isinstance(stream_properties, dict):
            stream_properties = StreamProperties(**stream_properties)
        if isinstance(table, dict):
            table = TableProps(**table)
        if __debug__:
            def stub(
                *,
                data_drop_tier: DataTier,
                destination_prefix: builtins.str,
                name: builtins.str,
                type: DataPipelineType,
                jdbc_properties: typing.Optional[typing.Union[JDBCProperties, typing.Dict[str, typing.Any]]] = None,
                job: typing.Optional[typing.Union[JobProperties, typing.Dict[str, typing.Any]]] = None,
                s3_properties: typing.Optional[typing.Union["S3Properties", typing.Dict[str, typing.Any]]] = None,
                stream_properties: typing.Optional[typing.Union["StreamProperties", typing.Dict[str, typing.Any]]] = None,
                table: typing.Optional[typing.Union["TableProps", typing.Dict[str, typing.Any]]] = None,
                tiers: typing.Optional[typing.Sequence[DataTier]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument data_drop_tier", value=data_drop_tier, expected_type=type_hints["data_drop_tier"])
            check_type(argname="argument destination_prefix", value=destination_prefix, expected_type=type_hints["destination_prefix"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument jdbc_properties", value=jdbc_properties, expected_type=type_hints["jdbc_properties"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument s3_properties", value=s3_properties, expected_type=type_hints["s3_properties"])
            check_type(argname="argument stream_properties", value=stream_properties, expected_type=type_hints["stream_properties"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument tiers", value=tiers, expected_type=type_hints["tiers"])
        self._values: typing.Dict[str, typing.Any] = {
            "data_drop_tier": data_drop_tier,
            "destination_prefix": destination_prefix,
            "name": name,
            "type": type,
        }
        if jdbc_properties is not None:
            self._values["jdbc_properties"] = jdbc_properties
        if job is not None:
            self._values["job"] = job
        if s3_properties is not None:
            self._values["s3_properties"] = s3_properties
        if stream_properties is not None:
            self._values["stream_properties"] = stream_properties
        if table is not None:
            self._values["table"] = table
        if tiers is not None:
            self._values["tiers"] = tiers

    @builtins.property
    def data_drop_tier(self) -> DataTier:
        result = self._values.get("data_drop_tier")
        assert result is not None, "Required property 'data_drop_tier' is missing"
        return typing.cast(DataTier, result)

    @builtins.property
    def destination_prefix(self) -> builtins.str:
        result = self._values.get("destination_prefix")
        assert result is not None, "Required property 'destination_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> DataPipelineType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(DataPipelineType, result)

    @builtins.property
    def jdbc_properties(self) -> typing.Optional[JDBCProperties]:
        result = self._values.get("jdbc_properties")
        return typing.cast(typing.Optional[JDBCProperties], result)

    @builtins.property
    def job(self) -> typing.Optional[JobProperties]:
        result = self._values.get("job")
        return typing.cast(typing.Optional[JobProperties], result)

    @builtins.property
    def s3_properties(self) -> typing.Optional["S3Properties"]:
        result = self._values.get("s3_properties")
        return typing.cast(typing.Optional["S3Properties"], result)

    @builtins.property
    def stream_properties(self) -> typing.Optional["StreamProperties"]:
        result = self._values.get("stream_properties")
        return typing.cast(typing.Optional["StreamProperties"], result)

    @builtins.property
    def table(self) -> typing.Optional["TableProps"]:
        result = self._values.get("table")
        return typing.cast(typing.Optional["TableProps"], result)

    @builtins.property
    def tiers(self) -> typing.Optional[typing.List[DataTier]]:
        result = self._values.get("tiers")
        return typing.cast(typing.Optional[typing.List[DataTier]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.ProcessorType")
class ProcessorType(enum.Enum):
    LAMBDA = "LAMBDA"


class S3DeliveryStream(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@randyridgley/cdk-datalake-constructs.S3DeliveryStream",
):
    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        kinesis_stream: aws_cdk.aws_kinesis.Stream,
        s3_bucket: aws_cdk.aws_s3.IBucket,
        compression: typing.Optional[CompressionType] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        transform_function: typing.Optional[aws_cdk.aws_lambda.Function] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param kinesis_stream: 
        :param s3_bucket: 
        :param compression: 
        :param s3_prefix: 
        :param transform_function: 
        '''
        if __debug__:
            def stub(
                parent: constructs.Construct,
                name: builtins.str,
                *,
                kinesis_stream: aws_cdk.aws_kinesis.Stream,
                s3_bucket: aws_cdk.aws_s3.IBucket,
                compression: typing.Optional[CompressionType] = None,
                s3_prefix: typing.Optional[builtins.str] = None,
                transform_function: typing.Optional[aws_cdk.aws_lambda.Function] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = DeliveryStreamProperties(
            kinesis_stream=kinesis_stream,
            s3_bucket=s3_bucket,
            compression=compression,
            s3_prefix=s3_prefix,
            transform_function=transform_function,
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            def stub(
                metric_name: builtins.str,
                *,
                account: typing.Optional[builtins.str] = None,
                color: typing.Optional[builtins.str] = None,
                dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                label: typing.Optional[builtins.str] = None,
                period: typing.Optional[aws_cdk.Duration] = None,
                region: typing.Optional[builtins.str] = None,
                statistic: typing.Optional[builtins.str] = None,
                unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Bytes", [props]))

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Records", [props]))

    @jsii.member(jsii_name="metricBackupToS3Success")
    def metric_backup_to_s3_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Success", [props]))

    @jsii.member(jsii_name="metricDataReadFromKinesisStreamBytes")
    def metric_data_read_from_kinesis_stream_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataReadFromKinesisStreamBytes", [props]))

    @jsii.member(jsii_name="metricDataReadFromKinesisStreamRecords")
    def metric_data_read_from_kinesis_stream_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDataReadFromKinesisStreamRecords", [props]))

    @jsii.member(jsii_name="metricDeliveryToS3Bytes")
    def metric_delivery_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDeliveryToS3Bytes", [props]))

    @jsii.member(jsii_name="metricDeliveryToS3DataFreshness")
    def metric_delivery_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDeliveryToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricDeliveryToS3Records")
    def metric_delivery_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDeliveryToS3Records", [props]))

    @jsii.member(jsii_name="metricDeliveryToS3Success")
    def metric_delivery_to_s3_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricDeliveryToS3Success", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.IBucket:
        return typing.cast(aws_cdk.aws_s3.IBucket, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: aws_cdk.aws_s3.IBucket) -> None:
        if __debug__:
            def stub(value: aws_cdk.aws_s3.IBucket) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogsRole")
    def _cloud_watch_logs_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return typing.cast(typing.Optional[aws_cdk.aws_iam.Role], jsii.get(self, "cloudWatchLogsRole"))

    @_cloud_watch_logs_role.setter
    def _cloud_watch_logs_role(
        self,
        value: typing.Optional[aws_cdk.aws_iam.Role],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[aws_cdk.aws_iam.Role]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogsRole", value)


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.S3Properties",
    jsii_struct_bases=[],
    name_mapping={
        "source_bucket_name": "sourceBucketName",
        "source_keys": "sourceKeys",
    },
)
class S3Properties:
    def __init__(
        self,
        *,
        source_bucket_name: builtins.str,
        source_keys: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param source_bucket_name: 
        :param source_keys: 
        '''
        if __debug__:
            def stub(
                *,
                source_bucket_name: builtins.str,
                source_keys: typing.Sequence[builtins.str],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument source_bucket_name", value=source_bucket_name, expected_type=type_hints["source_bucket_name"])
            check_type(argname="argument source_keys", value=source_keys, expected_type=type_hints["source_keys"])
        self._values: typing.Dict[str, typing.Any] = {
            "source_bucket_name": source_bucket_name,
            "source_keys": source_keys,
        }

    @builtins.property
    def source_bucket_name(self) -> builtins.str:
        result = self._values.get("source_bucket_name")
        assert result is not None, "Required property 'source_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_keys(self) -> typing.List[builtins.str]:
        result = self._values.get("source_keys")
        assert result is not None, "Required property 'source_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Properties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@randyridgley/cdk-datalake-constructs.Stage")
class Stage(enum.Enum):
    ALPHA = "ALPHA"
    BETA = "BETA"
    GAMMA = "GAMMA"
    PROD = "PROD"


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.StreamProperties",
    jsii_struct_bases=[],
    name_mapping={
        "stream_name": "streamName",
        "lambda_data_generator": "lambdaDataGenerator",
    },
)
class StreamProperties:
    def __init__(
        self,
        *,
        stream_name: builtins.str,
        lambda_data_generator: typing.Optional[typing.Union[LambdaDataGeneratorProperties, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param stream_name: 
        :param lambda_data_generator: 
        '''
        if isinstance(lambda_data_generator, dict):
            lambda_data_generator = LambdaDataGeneratorProperties(**lambda_data_generator)
        if __debug__:
            def stub(
                *,
                stream_name: builtins.str,
                lambda_data_generator: typing.Optional[typing.Union[LambdaDataGeneratorProperties, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument lambda_data_generator", value=lambda_data_generator, expected_type=type_hints["lambda_data_generator"])
        self._values: typing.Dict[str, typing.Any] = {
            "stream_name": stream_name,
        }
        if lambda_data_generator is not None:
            self._values["lambda_data_generator"] = lambda_data_generator

    @builtins.property
    def stream_name(self) -> builtins.str:
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_data_generator(self) -> typing.Optional[LambdaDataGeneratorProperties]:
        result = self._values.get("lambda_data_generator")
        return typing.cast(typing.Optional[LambdaDataGeneratorProperties], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@randyridgley/cdk-datalake-constructs.TableProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "columns": "columns",
        "description": "description",
        "input_format": "inputFormat",
        "output_format": "outputFormat",
        "parameters": "parameters",
        "partition_keys": "partitionKeys",
        "serde_parameters": "serdeParameters",
        "serialization_library": "serializationLibrary",
        "table_name": "tableName",
    },
)
class TableProps:
    def __init__(
        self,
        *,
        catalog_id: builtins.str,
        columns: typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]],
        description: builtins.str,
        input_format: builtins.str,
        output_format: builtins.str,
        parameters: typing.Mapping[builtins.str, typing.Any],
        partition_keys: typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]],
        serde_parameters: typing.Mapping[builtins.str, typing.Any],
        serialization_library: builtins.str,
        table_name: builtins.str,
    ) -> None:
        '''
        :param catalog_id: 
        :param columns: 
        :param description: 
        :param input_format: 
        :param output_format: 
        :param parameters: 
        :param partition_keys: 
        :param serde_parameters: 
        :param serialization_library: 
        :param table_name: 
        '''
        if __debug__:
            def stub(
                *,
                catalog_id: builtins.str,
                columns: typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]],
                description: builtins.str,
                input_format: builtins.str,
                output_format: builtins.str,
                parameters: typing.Mapping[builtins.str, typing.Any],
                partition_keys: typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]],
                serde_parameters: typing.Mapping[builtins.str, typing.Any],
                serialization_library: builtins.str,
                table_name: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument serde_parameters", value=serde_parameters, expected_type=type_hints["serde_parameters"])
            check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "catalog_id": catalog_id,
            "columns": columns,
            "description": description,
            "input_format": input_format,
            "output_format": output_format,
            "parameters": parameters,
            "partition_keys": partition_keys,
            "serde_parameters": serde_parameters,
            "serialization_library": serialization_library,
            "table_name": table_name,
        }

    @builtins.property
    def catalog_id(self) -> builtins.str:
        result = self._values.get("catalog_id")
        assert result is not None, "Required property 'catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def columns(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]], result)

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_format(self) -> builtins.str:
        result = self._values.get("input_format")
        assert result is not None, "Required property 'input_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_format(self) -> builtins.str:
        result = self._values.get("output_format")
        assert result is not None, "Required property 'output_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def partition_keys(
        self,
    ) -> typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]]:
        result = self._values.get("partition_keys")
        assert result is not None, "Required property 'partition_keys' is missing"
        return typing.cast(typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_glue.CfnTable.ColumnProperty, aws_cdk.IResolvable]]], result)

    @builtins.property
    def serde_parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        result = self._values.get("serde_parameters")
        assert result is not None, "Required property 'serde_parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def serialization_library(self) -> builtins.str:
        result = self._values.get("serialization_library")
        assert result is not None, "Required property 'serialization_library' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CompressionType",
    "CrossAccountProperties",
    "DataCatalogOwner",
    "DataLake",
    "DataLakeAdministrator",
    "DataLakeAdministratorProps",
    "DataLakeAnalyst",
    "DataLakeAnalystProps",
    "DataLakeBucket",
    "DataLakeBucketProps",
    "DataLakeCreator",
    "DataLakeCreatorProperties",
    "DataLakeProperties",
    "DataPipelineType",
    "DataProduct",
    "DataProductProperties",
    "DataSetResult",
    "DataStreamProperties",
    "DataTier",
    "DataTierBucketProps",
    "DeliveryStreamProperties",
    "DeliveryStreamType",
    "GlueCrawler",
    "GlueJob",
    "GlueJobOps",
    "GlueJobProperties",
    "GlueJobType",
    "GlueTable",
    "GlueVersion",
    "GlueWorkerType",
    "IGlueCrawlerProperties",
    "IGlueOpsProperties",
    "IGlueTableProperties",
    "IKinesisOpsProperties",
    "JDBCProperties",
    "JobProperties",
    "KinesisOps",
    "KinesisStream",
    "LakeKind",
    "LambdaDataGeneratorProperties",
    "NameBuilderParameters",
    "Permissions",
    "Pipeline",
    "PipelineProperties",
    "ProcessorType",
    "S3DeliveryStream",
    "S3Properties",
    "Stage",
    "StreamProperties",
    "TableProps",
]

publication.publish()
