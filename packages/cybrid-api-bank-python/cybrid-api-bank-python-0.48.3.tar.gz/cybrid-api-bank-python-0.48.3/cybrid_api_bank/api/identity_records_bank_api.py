"""
    Cybrid Bank API

    # Cybrid API documentation  Welcome to Cybrid, an all-in-one crypto platform that enables you to easily **build** and **launch** white-label crypto products or services.  In these documents, you'll find details on how our REST API operates and generally how our platform functions.  If you're looking for our UI SDK Widgets for Web or Mobile (iOS/Android), generated API clients, or demo applications, head over to our [Github repo](https://github.com/Cybrid-app).  💡 We recommend bookmarking the [Cybrid LinkTree](https://linktr.ee/cybridtechnologies) which contains many helpful links to platform resources.  ## Getting Started  This is Cybrid's public interactive API documentation, which allows you to fully test our APIs. If you'd like to use a different tool to exercise our APIs, you can download the [Open API 3.0 yaml](https://bank.demo.cybrid.app/api/schema/v1/swagger.yaml) for import.  If you're new to our APIs and the Cybrid Platform, follow the below guides to get set up and familiar with the platform:  1. [Getting Started in the Cybrid Sandbox](https://www.cybrid.xyz/guides/getting-started) 2. [Getting Ready for Trading](https://www.cybrid.xyz/guides/getting-ready-for-trading) 3. [Running the Web Demo App](https://www.cybrid.xyz/guides/running-the-cybrid-web-demo-crypto-app) (or, alternatively, [Testing with Hosted Web Demo App](https://www.cybrid.xyz/guides/testing-with-the-web-demo-crypo-app))  In [Getting Started in the Cybrid Sandbox](https://www.cybrid.xyz/guides/getting-started), we walk you through how to use the [Cybrid Sandbox](https://id.demo.cybrid.app/) to create a test bank, generate API keys, and set banks fees. In [Getting Ready for Trading](https://www.cybrid.xyz/guides/getting-ready-for-trading), we walk through creating customers, customer identities, accounts, as well as executing quotes and trades.  If you've already run through the first two guides, you can follow the [Running the Web Demo App](https://www.cybrid.xyz/guides/running-the-cybrid-web-demo-crypto-app) guide to test our web SDK with your sandbox `bank` and `customer`.  ## Working with the Cybrid Platform  There are three primary ways you can interact with the Cybrid platform:  1. Directly via our RESTful API (this documentation) 2. Using our API clients available in a variety of languages ([Angular](https://github.com/Cybrid-app/cybrid-api-bank-angular), [Java](https://github.com/Cybrid-app/cybrid-api-bank-java), [Kotlin](https://github.com/Cybrid-app/cybrid-api-bank-kotlin), [Python](https://github.com/Cybrid-app/cybrid-api-bank-python), [Ruby](https://github.com/Cybrid-app/cybrid-api-bank-ruby), [Swift](https://github.com/Cybrid-app/cybrid-api-bank-swift) or [Typescript](https://github.com/Cybrid-app/cybrid-api-bank-typescript)) 3. Integrating a platform specific SDK ([Web](https://github.com/Cybrid-app/cybrid-sdk-web), [Android](https://github.com/Cybrid-app/cybrid-sdk-android), Apple-coming soon)  Our complete set of APIs allows you to manage resources across three distinct areas: your `Organization`, your `Banks` and your `Identities`. For most of your testing and interaction you'll be using the `Bank` API, which is where the majority of APIs reside.  *The complete set of APIs can be found on the following pages:*  | API                                                              | Description                                                 | |------------------------------------------------------------------|-------------------------------------------------------------| | [Organization API](https://organization.demo.cybrid.app/api/schema/swagger-ui)   | APIs to manage organizations                                | | [Bank API](https://bank.demo.cybrid.app/api/schema/swagger-ui)                   | APIs to manage banks (and all downstream customer activity) | | [Identities API](https://id.demo.cybrid.app/api/schema/swagger-ui)                       | APIs to manage organization and bank identities             |  For questions please contact [Support](mailto:support@cybrid.xyz) at any time for assistance, or contact the [Product Team](mailto:product@cybrid.xyz) for product suggestions.  ## Authenticating with the API  The Cybrid Platform uses OAuth 2.0 Bearer Tokens to authenticate requests to the platform. Credentials to create `Organization` and `Bank` tokens can be generated via the [Cybrid Sandbox](https://id.demo.cybrid.app). Access tokens can be generated for a `Customer` as well via the [Cybrid IdP](https://id.demo.cybrid.app) as well.  An `Organization` access token applies broadly to the whole Organization and all of its `Banks`, whereas, a `Bank` access token is specific to an individual Bank. `Customer` tokens, similarly, are scoped to a specific customer in a bank.  Both `Organization` and `Bank` tokens can be created using the OAuth Client Credential Grant flow. Each Organization and Bank has its own unique `Client ID` and `Secret` that allows for machine-to-machine authentication.  A `Bank` can then generate `Customer` access tokens via API.  <font color=\"orange\">**⚠️ Never share your Client ID or Secret publicly or in your source code repository.**</font>  Your `Client ID` and `Secret` can be exchanged for a time-limited `Bearer Token` by interacting with the Cybrid Identity Provider or through interacting with the **Authorize** button in this document.  The following curl command can be used to quickly generate a `Bearer Token` for use in testing the API or demo applications.  ``` curl -X POST https://id.demo.cybrid.app/oauth/token -d '{     \"grant_type\": \"client_credentials\",     \"client_id\": \"<Your Client ID>\",     \"client_secret\": \"<Your Secret>\",     \"scope\": \"banks:read banks:write accounts:read accounts:execute customers:read customers:write customers:execute prices:read quotes:execute trades:execute trades:read\"   }' -H \"Content-Type: application/json\" ``` <font color=\"orange\">**⚠️ Note: The above curl will create a bearer token with full scope access. Delete scopes if you'd like to restrict access.**</font>  ## Authentication Scopes  The Cybrid platform supports the use of scopes to control the level of access a token is limited to. Scopes do not grant access to resources; instead, they provide limits, in support of the least privilege principal.  The following scopes are available on the platform and can be requested when generating either an Organization or a Bank token. Generally speaking, the _Read_ scope is required to read and list resources, the _Write_ scope is required to update a resource and the _Execute_ scope is required to create a resource.  | Resource               | Read scope (Token Type)                                    | Write scope (Token Type)           | Execute scope (Token Type)                      | |------------------------|------------------------------------------------------------|------------------------------------|-------------------------------------------------| | Organizations          | organizations:read (Organization)                          | organizations:write (Organization) |                                                 | | Banks                  | banks:read (Organization, Bank)                            | banks:write (Organization, Bank)   | banks:execute (Organization)                    | | Customers              | customers:read (Organization, Bank, Customer)              | customers:write (Bank)             | customers:execute (Bank)                        | | Accounts               | accounts:read (Organization, Bank, Customer)               |                                    | accounts:execute (Bank, Customer)               | | Prices                 | prices:read (Bank, Customer)                               |                                    |                                                 | | Quotes                 | quotes:read (Organization, Bank, Customer)                 |                                    | quotes:execute (Bank, Customer)                 | | Trades                 | trades:read (Organization, Bank, Customer)                 |                                    | trades:execute (Bank)                           | | Rewards                | rewards:read (Bank)                                        |                                    | rewards:execute (Bank)                          | | External bank accounts | external_bank_accounts:read (Organization, Bank, Customer) |                                    | external_bank_accounts:execute (Bank, Customer) |  ## Available Endpoints  The available APIs for the [Identity](https://id.demo.cybrid.app/api/schema/swagger-ui), [Organization](https://organization.demo.cybrid.app/api/schema/swagger-ui) and [Bank](https://bank.demo.cybrid.app/api/schema/swagger-ui) API services are listed below:  | API Service  | Model               | API Endpoint Path              | Description                                                                                       | |--------------|---------------------|--------------------------------|---------------------------------------------------------------------------------------------------| | Identity     | Bank                | /api/bank_applications         | Create and list banks                                                                             | | Identity     | Organization        | /api/organization_applications | Create and list organizations                                                                     | | Identity     | CustomerToken       | /api/customer_tokens           | Create customer JWT access tokens                                                                 | | Organization | Organization        | /api/organizations             | APIs to retrieve and update organization name                                                     | | Bank         | Asset               | /api/assets                    | Get a list of assets supported by the platform (ex: BTC, ETH)                                     | | Bank         | VerificationKey     | /api/bank_verification_keys    | Create, list and retrive verification keys, used for signing identities                           | | Bank         | Banks               | /api/banks                     | Create, update and list banks, the parent to customers, accounts, etc                             | | Bank         | FeeConfiguration    | /api/fee_configurations        | Create and list bank fees (spread or fixed)                                                       | | Bank         | Customers           | /api/customers                 | Create and list customers                                                                         | | Bank         | IdentityRecord      | /api/identity_records          | Create and list identity records, which are attached to customers for KYC                         | | Bank         | Accounts            | /api/accounts                  | Create and list accounts, which hold a specific asset for a customers                             | | Bank         | Symbols             | /api/symbols                   | Get a list of symbols supported for trade (ex: BTC-USD)                                           | | Bank         | Prices              | /api/prices                    | Get the current prices for assets on the platform                                                 | | Bank         | Quotes              | /api/quotes                    | Create and list quotes, which are required to execute trades                                      | | Bank         | Trades              | /api/trades                    | Create and list trades, which buy or sell cryptocurrency                                          | | Bank         | Rewards             | /api/rewards                   | Create a new reward (automates quote/trade for simplicity)                                        | | Bank         | ExternalBankAccount | /api/external_bank_account     | Create, get and list external bank accounts, which connect customer bank accounts to the platform |  ## Understanding Object Models & Endpoints  **Organizations**  An `Organization` is meant to represent the organization partnering with Cybrid to use our platform.  An `Organization` does not directly interact with `customers`. Instead, an Organization has one or more `banks`, which encompass the financial service offerings of the platform.  **Banks**  A `Bank` is owned by an `Organization` and can be thought of as an environment or container for `Customers` and product offerings. Banks are created in either `Sandbox` or `Production` mode, where Sandbox is the environment that you would test, prototype and build in prior to production.  An `Organization` can have multiple `banks`, in either sandbox or production environments. A sandbox Bank will be backed by stubbed data and process flows. For instance, funding source processes will be simulated rather than performed, however asset prices are representative of real-world values. You have an unlimited amout of simulated fiat currency for testing purposes.  ## Customers  `Customers` represent your banking users on the platform. At present, we offer support for `Individuals` as Customers.  `Customers` must be verified in our system before they can play any part on the platform, which means they must have an associated and valid `Identity Record`. See the Identity Records section for more details on how a customer can be verified.  `Customers` must also have an `account` to be able to transact, in the desired asset class. See the Accounts APIs for more details on setting up accounts for the customer.   # noqa: E501

    The version of the OpenAPI document: v0.48.3
    Contact: support@cybrid.app
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from cybrid_api_bank.api_client import ApiClient, Endpoint as _Endpoint
from cybrid_api_bank.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from cybrid_api_bank.model.error_response import ErrorResponse
from cybrid_api_bank.model.identity_record import IdentityRecord
from cybrid_api_bank.model.identity_record_list import IdentityRecordList
from cybrid_api_bank.model.post_identity_record import PostIdentityRecord


class IdentityRecordsBankApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_identity_record_endpoint = _Endpoint(
            settings={
                'response_type': (IdentityRecord,),
                'auth': [
                    'BearerAuth',
                    'oauth2'
                ],
                'endpoint_path': '/api/identity_records',
                'operation_id': 'create_identity_record',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'post_identity_record',
                ],
                'required': [
                    'post_identity_record',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'post_identity_record':
                        (PostIdentityRecord,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'post_identity_record': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.get_identity_record_endpoint = _Endpoint(
            settings={
                'response_type': (IdentityRecord,),
                'auth': [
                    'BearerAuth',
                    'oauth2'
                ],
                'endpoint_path': '/api/identity_records/{identity_record_guid}',
                'operation_id': 'get_identity_record',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'identity_record_guid',
                ],
                'required': [
                    'identity_record_guid',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'identity_record_guid':
                        (str,),
                },
                'attribute_map': {
                    'identity_record_guid': 'identity_record_guid',
                },
                'location_map': {
                    'identity_record_guid': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_identity_records_endpoint = _Endpoint(
            settings={
                'response_type': (IdentityRecordList,),
                'auth': [
                    'BearerAuth',
                    'oauth2'
                ],
                'endpoint_path': '/api/identity_records',
                'operation_id': 'list_identity_records',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'customer_guid',
                    'page',
                    'per_page',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'page',
                    'per_page',
                ]
            },
            root_map={
                'validations': {
                    ('page',): {

                        'inclusive_minimum': 0,
                    },
                    ('per_page',): {

                        'inclusive_maximum': 100,
                        'inclusive_minimum': 1,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'customer_guid':
                        (str,),
                    'page':
                        (int,),
                    'per_page':
                        (int,),
                },
                'attribute_map': {
                    'customer_guid': 'customer_guid',
                    'page': 'page',
                    'per_page': 'per_page',
                },
                'location_map': {
                    'customer_guid': 'query',
                    'page': 'query',
                    'per_page': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def create_identity_record(
        self,
        post_identity_record,
        **kwargs
    ):
        """Create Identity Record  # noqa: E501

        Creates an identity record.  ## Identity Records  Identity Records verify an individual for inclusion on the platform. This know-your-customer (KYC) process is a requirement for individuals to be able to transact. At present, we offer support for Attestation Identity Records.  Once an Identity Record has been submitted, it will be reviewed by our system and transit through a lifecycle before ultimately being `verified` or `failed`. If an Identity Record is ends up `failed`, contextual information as to the reason may be provided on the resource and additional attempts can be made.  ## Attestation Identity Records  An Attestation Identity Record is a confirmation of fact that the Organization has completed their own KYC process and can vouch for its correctness.  Prior to uploading `verified` attestation identity records, an Organization must register their signing public key with their Bank through the create Verification Key API.  To create an attestation identity record, a signed JWT is required as proof that the Customer's identity has been verified by the Organization. When creating the JWT, the Organization must use the RS512 signing algorithm.  The JWT must contain the following headers:  - **alg**: The RS512 algorithm value, e.g., 'RS512'. - **kid**: Set to the guid of the verification key that has been registered for the Bank  The JWT must contain the following claims:  - **iss**: Set to http://api.cybrid.app/banks/{bank_guid} - **aud**: Set to http://api.cybrid.app - **sub**: Set to http://api.cybrid.app/customers/{customer_guid} - **iat**: Set to the time at which the JWT was issued - **exp**: Set to the time after which the JWT expires - **jti**: Set to a unique identifier for the JWT  Example code (python) for generating an Attestation Identity Record JWT token:  ```python # Assumes an RSA private key has been generated (`private_key`), a Verification Key has been created and a `verification_key_guid` is available. # # `customer_guid` should be set to the guid assigned to a Customer that has been created. # `bank_guid` should be set to the guid of your bank #  import uuid  from datetime import datetime, timezone, timedelta from jwcrypto import jwt, jwk from cryptography.hazmat.primitives import serialization from cryptography.hazmat.primitives.serialization import load_pem_private_key  algorithm = 'RS512' issued_at = datetime.now(timezone.utc) expired_at = issued_at + timedelta(days=365)  with open(\"verification_key.pem\", 'rb') as pem_in:   pem_lines = pem_in.read()  private_key = load_pem_private_key(pem_lines, None)  ### DISCLAIMER:- Since NO ENCRYPTION is used in the key storage/formatting. Please DO NOT use this code in production environment. signing_key = jwk.JWK.from_pem(     private_key.private_bytes(         encoding=serialization.Encoding.PEM,         format=serialization.PrivateFormat.PKCS8,         encryption_algorithm=serialization.NoEncryption()     ) ) signing_key.update({\"kid\": verification_key_guid})  attestation_jwt = jwt.JWT(     header={         \"alg\": algorithm,         \"kid\": verification_key_guid     },     claims={         \"iss\": f\"http://api.cybrid.app/banks/{bank_guid}\",         \"aud\": \"http://api.cybrid.app\",         \"sub\": f\"http://api.cybrid.app/customers/{customer_guid}\",         \"iat\": int(issued_at.timestamp()),         \"exp\": int(expired_at.timestamp()),         \"jti\": str(uuid.uuid4())     },     key=signing_key,     algs=[algorithm] ) attestation_jwt.make_signed_token(signing_key)  token = attestation_jwt.serialize(compact=True) print(\"Token is : \", token) ```  ## Default Attestation Signing Key  The Cybrid Sandbox environment comes provisioned with a default signing key that can be used to perform identity record attestation. The default identity signing key provides a convenient starting point for testing Sandbox flows that require identity attestation, such as executing trades.  The signing key can be loaded directly into a client application by passing its PEM encoded value as an environment variable.  ``` -----BEGIN PRIVATE KEY----- MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDZ75nSfJy/eeuj 4f7EK7i+n4FUDE8BsD/acCdk9Pn56suuDc3SFcMoyjBIoDLZkbRsVfmBEcPDNJOp GNqzoaXa7qe7Yw0qpK9MbNbAYxiyAfxwVHM+ZpwP6M/r3LmsCRFXgNdCjfOzok7u V59hDjfHMMQm/M9ztGVhaJpgozY/7DKk+R6qY/DEBs63eXwfcHE0u0NbS8Y9Qp+6 7cB2f1iuy++5Uut1vx4qdgZ4UFMkwIdTWl/e6LDcdXhk3///T5WOnDlI+S4rhGUO xsAOfOa+T9uqYBr2hbQR9emTEYmwF1lgZ7VU4S9sSjAMKpB/TVlVVOsNhdNSGg6f 6hu7fuadAgMBAAECggEBAMUJL1VyfHVRUY5VoPTTYrBVnaPTjQrFwrVHeRZ5thgS BBxVNqSeMFgMlSLUU6UJasoX4QCkgw1V17qmUfTeTQlnhBaTMzA+vI6oSHCgJ4+o 5AbbE2Zzdt2ba4Cfiu7TM+6c+gGePZtHP32Vku84340jtfRZ1WWSz6YF4K1GYqHe y7I4POotHu2WcSTXYKs2zTu5KAO7gvx7yITVytaiUGUHk9FNyZPDIh0u7e9CAEti BangdYTfvbXAIx9lrg3XQ4gtFXTd0aY/3R9K3SE+s5iWh/SabjV4U7x+MuHZS5kv 8rcLCPQ5kUgiF4bQMy7QznUuNso65SbRJKHaU8UAuIECgYEA7+bNdz/uiN/JxUJY 3xwjD+CG4vXOyEmCioBjllYBeXQyB/VrsdzVrdF2JiECnStPRH6/6nd7/wUcLORv NyrQqnCa5/O8Kv9Z3t4TmxYf+ECIgx+gazehQHptUkr8QWtxceorUC9pu4cUJ8z3 nQLCggHYQ3g7xj73LLZ+5QQBC8kCgYEA6I91Dgs+HZWDMMcGbKV2cMkXK8BTOgZZ 6B6i6flO4tf9U2CPBZsjYLBN5EEuxxy9Yl7rlV7CxAhnnjdIKk2jQbzTPI0qmJfp 397rvdR8bur1OkALj2Tb39fz8z1Qy7AcN8siqXuortZZ5OI9XRWgnG/3B4gUFOnW 4Mr0dhfaxjUCgYEAmVcricehjneMnrtz1thDSQi47yUzES57dE/wV82Nj7ZHrHKg bcW8ByhVnrWG2DMwrZVe0l2hMjZv9fnlZJvHWMo1GYHfipRBO4UzfvO7Z5DIMRfs D9w1A+O9MNahOqeUkb2eBdjoemcy6OXId+Gltje7phSaEHN6xme34GaYzJECgYBP eRbLYdQsT/exJ5JudmzvRgkBDoxie+EljbKmumfW5XDQmWLGy6lfVWCI7C2MJaoi f8WKGgP88dJXIxUqP7XWtSyKuMMhumhV9Nwi1wZe8TQ0X8aTjigFassXCJEfymMa PfTubi/K771wlk/aC5YDX8/PZxVVwEOKNlEsOiKtMQKBgQDqRv5AUHhabqcMfbs7 DTeo/fS/eXJv8MN+CUU2RSrNUKjEdHT2R5KP550TyXr1JXLKpEEZu8wvvaQDV4Dw p0Eij6bKsh03X38NR+C5SxonXPosdvoiXR8uUgya2f/aJYV+aWZ9euFgYZAXf/0Q MnWdKylfZlV50XP2KFn07wPs7w== -----END PRIVATE KEY----- ```  A corresponding public verification key can be retrieved from the Cybrid Banks API using the `/api/bank_verification_keys` endpoint. Performing a `get` request to this endpoint returns the available Verification Key records, the first of which is the provisioned default. The endpoint can be hit directly or by using the Cybrid Banks API client:  ```python ... api_client = cybrid_api_bank.ApiClient(configuration) api_instance = verification_keys_bank_api.VerificationKeysBankApi(api_client) verification_keys = api_instance.list_verification_keys() verification_key = verification_keys.objects[0] ```  Once available to the application, the signing key and Verification Key record can be used in conjunction to create the attestation JWT. The Verification Key's GUID is passed as the JWT's `kid` while the signing key is used to sign the JWT.  ## Attestation State  | State | Description | |-------|-------------| | storing | The Platform is storing the attestation in our private store | | pending | The Platform is verifying the attestation's JWT | | verified | The Platform has verified the attestation and the customer is able to transact | | failed | The Platform was not able to verify the attestation and the customer is not able to transact |    Required scope: **customers:write**  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_identity_record(post_identity_record, async_req=True)
        >>> result = thread.get()

        Args:
            post_identity_record (PostIdentityRecord):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            IdentityRecord
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['post_identity_record'] = \
            post_identity_record
        return self.create_identity_record_endpoint.call_with_http_info(**kwargs)

    def get_identity_record(
        self,
        identity_record_guid,
        **kwargs
    ):
        """Get Identity Record  # noqa: E501

        Retrieves an identity record.  Required scope: **customers:read**  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_identity_record(identity_record_guid, async_req=True)
        >>> result = thread.get()

        Args:
            identity_record_guid (str): Identifier for the identity record.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            IdentityRecord
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['identity_record_guid'] = \
            identity_record_guid
        return self.get_identity_record_endpoint.call_with_http_info(**kwargs)

    def list_identity_records(
        self,
        **kwargs
    ):
        """List Identity Records  # noqa: E501

        Retrieves a listing of identity records for a bank.  Required scope: **customers:read**  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_identity_records(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            customer_guid (str): Comma separated customer identifier to list identity records for.. [optional]
            page (int): [optional]
            per_page (int): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            IdentityRecordList
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        return self.list_identity_records_endpoint.call_with_http_info(**kwargs)

