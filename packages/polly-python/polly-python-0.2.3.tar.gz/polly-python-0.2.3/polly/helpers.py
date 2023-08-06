import base64
import os
import re
import json
import logging
import requests
import urllib.request
from cloudpathlib import S3Client
from botocore.exceptions import ClientError
from cmapPy.pandasGEXpress.parse_gct import parse
from os import environ
from jose import jwt
from polly.errors import (
    BadRequestError,
    error_handler,
    InvalidParameterException,
    MissingKeyException,
    InvalidPathException,
    OperationFailedException,
    paramException,
    AccessDeniedError,
    InvalidRepoException,
)
from polly.constants import COHORT_CONSTANTS_URL, REPORT_FIELDS_URL, ELUCIDATA_LOGO_URL
from bs4 import BeautifulSoup
import contextlib
import joblib
import urllib


def get_platform_value_from_env(
    variable: str, default_val: str, passed_val: str
) -> str:
    """
    Get variable value of passed variable
    from os env variables
    """
    if passed_val:
        default_val = passed_val
    elif environ.get(variable, None) is not None:
        POLLY_TYPE = os.getenv(variable)
        env_val = re.search("https://(.+?).elucidata.io", POLLY_TYPE)
        default_val = env_val.group(1)
    return default_val


def make_path(prefix: any, postfix: any) -> str:
    """
    Function to make and return a valid path
    """
    if not prefix:
        raise InvalidParameterException("prefix")
    if not postfix:
        raise InvalidParameterException("postfix")
    return os.path.normpath(f"{prefix}/{postfix}")


def get_sts_creds(sts_dict: dict) -> dict:
    """
    Function to check and return temporary sts creds
    """
    if sts_dict and isinstance(sts_dict, dict):
        if "data" in sts_dict:
            data = sts_dict.get("data")
            if "attributes" in data[0]:
                attributes = data[0].get("attributes")
                if "credentials" in attributes:
                    return attributes.get("credentials")
                else:
                    raise MissingKeyException("credentials")
            else:
                raise MissingKeyException("attributes")
        else:
            raise MissingKeyException("data")
    else:
        raise InvalidParameterException("sts_dict")


def upload_to_S3(cloud_path: str, local_path: str, credentials: dict) -> None:
    """
    Function to upload file/folder to S3 cloud path
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        source_path.mkdir()
    try:
        source_path.upload_from(local_path, force_overwrite_to_cloud=True)
    except ClientError as e:
        raise OperationFailedException(e)


def download_from_S3(cloud_path: str, workspace_path: str, credentials: dict) -> None:
    """
    Function to download file/folder from workspaces
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        raise InvalidPathException
    isFile = source_path.is_file()
    if isFile:
        try:
            dest_path = os.getcwd()
            source_path.copy(dest_path, force_overwrite_to_cloud=True)
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Download successful to path={dest_path}")
        except ClientError as e:
            raise OperationFailedException(e)
    else:
        if not cloud_path.endswith("/"):
            cloud_path += "/"
        source_path = client.CloudPath(cloud_path)
        if not source_path.is_dir():
            raise InvalidPathException
        try:
            dest_path = f"{make_path(os.getcwd(),workspace_path)}"
            source_path.copytree(dest_path, force_overwrite_to_cloud=True)
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Download successful to path={dest_path}")
        except ClientError as e:
            raise OperationFailedException(e)


def get_workspace_payload(
    cloud_path: str, credentials: dict, source_key: str, source_path: str
):
    """
    Function to return payload for create_copy function
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if not source_path.exists():
        raise InvalidPathException
    isFile = source_path.is_file()
    if isFile:
        payload = {
            "data": [
                {
                    "attributes": {
                        "s3_key": source_key,
                    },
                    "id": "",
                    "type": "file",
                }
            ]
        }
    else:
        if not source_key.endswith("/"):
            source_key += "/"
        payload = {
            "data": [
                {
                    "attributes": {
                        "s3_key": source_key,
                    },
                    "id": "",
                    "type": "folder",
                }
            ]
        }
    return payload


def file_conversion(
    self, repo_info: str, dataset_id: str, format: str, header_mapping: dict
) -> None:
    """
    Function that converts file to mentioned format
    """
    if not (repo_info and isinstance(repo_info, str)):
        raise InvalidParameterException("repo_name/repo_id")
    if not (dataset_id and isinstance(dataset_id, str)):
        raise InvalidParameterException("dataset_id")
    if not (format and isinstance(format, str)):
        raise InvalidParameterException("format")
    if not isinstance(header_mapping, dict):
        raise InvalidParameterException("header_mapping")
    download_dict = self.download_data(repo_info, dataset_id)
    url = download_dict.get("data", {}).get("attributes", {}).get("download_url")
    if not url:
        raise MissingKeyException("dataset url")
    file_name = f"{dataset_id}.gct"
    try:
        urllib.request.urlretrieve(url, file_name)
        data = parse(file_name)
        os.remove(file_name)
        row_metadata = data.row_metadata_df
        if header_mapping:
            row_metadata = row_metadata.rename(header_mapping, axis=1)
        row_metadata.to_csv(f"{dataset_id}.{format}", sep="\t")
    except Exception as e:
        raise OperationFailedException(e)


def get_data_type(self, url: str, payload: dict) -> str:
    """
    Function to return the data-type of the required dataset
    """
    if not (url and isinstance(url, str)):
        raise InvalidParameterException("url")
    if not (payload and isinstance(payload, dict)):
        raise InvalidParameterException("payload")
    response = self.session.post(url, data=json.dumps(payload))
    error_handler(response)
    response_data = response.json()
    hits = response_data.get("hits", {}).get("hits")
    if not (hits and isinstance(hits, list)):
        raise paramException(
            title="Param Error",
            detail="No matches found with the given repo details. Please try again.",
        )
    dataset = hits[0]
    data_type = dataset.get("_source", {}).get("data_type")
    if not data_type:
        raise MissingKeyException("data_type")
    return data_type


def get_metadata(self, url: str, payload: dict) -> str:
    """
    Function to return the data-type of the required dataset
    """
    if not (url and isinstance(url, str)):
        raise InvalidParameterException("url")
    if not (payload and isinstance(payload, dict)):
        raise InvalidParameterException("payload")
    response = self.session.post(url, data=json.dumps(payload))
    error_handler(response)
    response_data = response.json()
    hits = response_data.get("hits", {}).get("hits")
    if not (hits and isinstance(hits, list)):
        raise paramException(
            title="Param Error",
            detail="No matches found with the given repo details. Please try again.",
        )
    dataset = hits[0]
    return dataset


def elastic_query(index_name: str, dataset_id: str) -> dict:
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"_index": index_name}},
                    {"term": {"dataset_id.keyword": dataset_id}},
                ]
            }
        }
    }
    return query


def get_cohort_constants() -> json:
    """
    Returns cohort info from public assests url
    """
    response = requests.get(COHORT_CONSTANTS_URL)
    error_handler(response)
    return json.loads(response.text)


def get_cohort_fields() -> json:
    """
    Returns file format info from public assests url
    """
    response = requests.get(REPORT_FIELDS_URL)
    error_handler(response)
    return json.loads(response.text)


def validate_datatype(datatype: str):
    """
    Function to validate datatype of a dataset
    Returns 1 in case of datatype is Single Cell, 0 otherwise
    """
    if datatype == "Single cell":
        return 1
    return 0


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""

    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def check_empty(x):
    """
    Function to validate if the entry is an empty list or not.
    """
    if type(x) == list:
        return len("".join(x))
    elif type(x) == float or type(x) == int:
        return 1
    else:
        return len(x)


def edit_html(local_path: str):
    """
    Function to include Elucidata logo into the report.
    """
    el_image = f"""
        <a>
        <img  style="margin-left: 25px;" src={ELUCIDATA_LOGO_URL}
        width=150" height="70" align="middle">
    </a>
    """
    id_soup = BeautifulSoup(el_image, "html.parser")
    with open(local_path) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    soup.body.insert(1, id_soup)
    with open(local_path, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


def verify_workspace_path(cloud_path: str, credentials: dict) -> tuple:
    """
    Function to verify if the workspace path is valid.
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if source_path.exists():
        return source_path, True
    else:
        return source_path, False


def check_is_file(self, sts_url: str, workspace_id: int, workspace_path: str) -> bool:
    """
    Function to check if the workspace_path is a valid file path existing in the workspace.
    """
    creds = self.session.get(sts_url)
    error_handler(creds)
    credentials = get_sts_creds(creds.json())
    if self.session.env == "polly":
        env_string = "prod"
    elif self.session.env == "testpolly":
        env_string = "test"
    else:
        env_string = "devenv"
    bucket = f"mithoo-{env_string}-project-data-v1"
    s3_path = f"{bucket}/{workspace_id}/"
    s3_path = f"s3://{make_path(s3_path, workspace_path)}"
    tuple_output = verify_workspace_path(s3_path, credentials)
    source_path = tuple_output[0]
    status = tuple_output[1]
    if status is True:
        isFile = source_path.is_file()
        return isFile
    return status


def split_workspace_path(absolute_path: str) -> tuple:
    """
    Function to separate workspace_id and workspace_path from s3 path
    """
    contents = absolute_path.split("/")
    workspace_id = contents[0]
    workspace_path = contents[1]
    for item in range(2, len(contents)):
        workspace_path = make_path(workspace_path, contents[item])
    return workspace_id, workspace_path


def make_private_link(workspace_id: int, workspace_path: str, constant_url: str) -> str:
    """
    Function to construct and return a private link for a file in workspace
    """
    file_element = {"file": f"/projects/{workspace_id}/files/{workspace_path}"}
    private_access_link = f"{constant_url}/workspaces?id={workspace_id}&{urllib.parse.urlencode(file_element)}&preview=true"
    return private_access_link


def change_file_access(
    self, access_key: str, workspace_id: int, workspace_path: str, access_url: str
) -> str:
    """
    Function to change the file access as per the access_key and returns the final access url
    """
    final_url = ""
    if access_key == "private":
        params = {"action": "share", "access_type": "private"}
        url = f"{self.base_url}/projects/{workspace_id}/files/{workspace_path}"
        # API call to change the file access to private
        response = self.session.get(url, params=params)
        error_handler(response)
        final_url = make_private_link(workspace_id, workspace_path, access_url)
    else:
        params = {"action": "share", "access_type": "global"}
        url = f"{self.base_url}/projects/{workspace_id}/files/{workspace_path}"
        # API call to change the file access to public
        response = self.session.get(url, params=params)
        error_handler(response)
        shared_id = response.json().get("data").get("shared_id")
        final_url = f"{access_url}/shared/file/?id={shared_id}"
    return final_url


def get_user_details(self):
    """
    Function to get user details
    """
    me_url = f"{self.base_url}/users/me"
    details = self.session.get(me_url)
    error_handler(details)
    user_details = details.json().get("data", {}).get("attributes")
    return user_details


def get_user_details_using_aws_cognito(self):
    """
    Summary :
    gets the user details such as sub, aud post verification
    using aws cognito

    Returns:
        dictionary of token keys and values
    """
    # getting the userpool details
    pool_url = f"https://api.{self.session.env}.elucidata.io/userpool"
    pool_details = self.session.get(pool_url)
    pool_details_json = pool_details.json()
    user_pool_region = pool_details_json.get("cognito_user_pool_region", "")
    user_pool_id = pool_details_json.get("cognito_user_pool", "")
    # cognito_client_id = pool_details_json.get("cognito_client_id", "")
    session_cookies_dict = self.session.cookies.get_dict()
    id_token = session_cookies_dict.get("idToken", "")
    session_headers_dict = self.session.headers
    cookie = session_headers_dict.get("Cookie", "")
    # cookie is a string
    if "refreshToken=" in cookie:
        refresh_token = cookie.split("refreshToken=")[1]
    else:
        print("refresh token not presen in header cookie")
        refresh_token = ""

    # Getting Headers
    # headers = jwt.get_unverified_header(id_token)
    kid = get_value_from_idToken(id_token, "kid")

    # Getting Pool Url
    verify_url = generate_aws_pool_url(user_pool_region, user_pool_id)

    kargs = {"issuer": verify_url}
    kargs["options"] = {"verify_at_hash": False}
    kargs["audience"] = get_value_from_idToken(id_token, "aud")
    keys = aws_key_dict(user_pool_region, user_pool_id)

    # Get Public Key
    public_key = get_public_key(keys, kid)

    decoded_token = jwt.decode(id_token, public_key, **kargs)
    decoded_token["id_token"] = id_token
    decoded_token["refresh_token"] = refresh_token

    return decoded_token


def generate_aws_pool_url(user_pool_region, user_pool_id):
    verify_url = "https://cognito-idp.{}.amazonaws.com/{}".format(
        user_pool_region, user_pool_id
    )
    return verify_url


def get_public_key(keys, kid):
    """
    Getting public key in pem format from Id Token

    Parameters
    ----------
    keys: Dict
        JWT headers keys
    kid: String
        public key identifier

    Returns
    ----------
    pubk_bytes: String (PEM)
        Public key in pem format
    """

    key = keys[kid]
    return key


def aws_key_dict(region, user_pool_id):
    """
    Fetches the AWS JWT validation file (if necessary) and then converts
    this file into a keyed dictionary that can be used to validate a web-token
    we've been passed

    Parameters
    ----------
    aws_user_pool: String
        AWS Cognito user pool ID
    aws_region: String
        AWS Cognito user pool region

    Returns:
    -------
    dict:
        Contains decoded token dict
    """
    filename = "/tmp/" + "aws_{}.json".format(user_pool_id)

    if not os.path.isfile(filename):
        # If we can't find the file already, try to download it.
        aws_data = requests.get(
            ("https://cognito-idp.{}.amazonaws.com/{}".format(region, user_pool_id))
            + "/.well-known/jwks.json"
        )
        aws_jwt = json.loads(aws_data.text)
        with open(filename, "w+") as json_data:
            json_data.write(aws_data.text)
            json_data.close()

    else:
        with open(filename) as json_data:
            aws_jwt = json.load(json_data)
            json_data.close()

    # We want a dictionary keyed by the kid, not a list.
    result = {}
    for item in aws_jwt["keys"]:
        result[item["kid"]] = item

    return result


def get_value_from_idToken(id_token: str, key: str) -> dict:
    decoded_id_token_dict = decode_id_token(id_token)
    return decoded_id_token_dict.get(key, "")


def decode_id_token(tokenID: str) -> dict:
    """
    Summary: decodes the token id
    this method is to decode the tokenID which consists of 3 parts.
    the first 2 parts can be base64 decoded
    first part contains the kid and alg details.
    second part contains cognito:user details (AWS) such as sub, username
    aud, name, exp, email etc.

    Args:
        tokenId : str

    Returns:
        dict of keys and values from decoded idToken
    """
    decoded_idToken_dict = {}
    try:
        for element in tokenID.split(".")[:2]:
            # the element if lacking "padding" can give 'incorrect padding' error.
            # to handle that we have add the extra padding of '='
            # the len of the element should always be a multiple of 4.
            # https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding

            decoded_str = base64.b64decode(element + "=" * (-len(element) % 4))
            decoded_idToken_dict.update(json.loads(decoded_str.decode("utf-8")))
    except Exception as err:
        print("something wrong with idToken")
        raise err
    return decoded_idToken_dict


def makeRequestCookieForPollyJob(job_data: json) -> json:

    """
    Generates the cookie required request for polly job API

    Args:
        Job data : Dict
    Returns:
        request_cookie: generated cookie string
    """

    secret_env_vars = job_data.get("secret_env", "")

    aud = secret_env_vars.get("POLLY_AUD", "")
    sub = secret_env_vars.get("POLLY_SUB", "")
    idToken = secret_env_vars.get("POLLY_ID_TOKEN", "")
    refreshToken = secret_env_vars.get("POLLY_REFRESH_TOKEN", "")
    idTokenCookie = f"CognitoIdentityServiceProvider.{aud}.{sub}.idToken={idToken}"
    refreshCookie = (
        f"CognitoIdentityServiceProvider.{aud}.{sub}.refreshToken={refreshToken}"
    )
    request_coookie = f"{idTokenCookie};{refreshCookie}"
    # print("returning request_coookie: " + request_coookie)
    return request_coookie


def workspaces_permission_check(self, workspace_id) -> bool:
    """
    Function to check access of a user for a given workspace id.
    """
    permission_url = f"{self.base_url}/workspaces/{workspace_id}/permissions"
    response = self.session.get(permission_url, params={"include": "user"})
    error_handler(response)
    user_details = get_user_details(self)
    user_id = user_details.get("user_id")
    if "data" in response.json():
        json_data = response.json().get("data")
    else:
        raise BadRequestError(detail="Incorrect response format")
    for user in json_data:
        if "attributes" in user:
            attributes = user.get("attributes")
        else:
            raise BadRequestError(detail="Incorrect response format")
        if user_id == attributes["user_id"] and attributes["project_id"] == int(
            workspace_id
        ):
            if attributes["permission"] != "read":
                return True
            else:
                raise AccessDeniedError(
                    detail=f"Read-only permission over the "
                    f"workspace-id {workspace_id}"
                )
    return False


def verify_workspace_details(self, workspace_id, workspace_path, sts_url) -> None:
    """
    Function to check and verify workspace permissions and workspace path.
    """
    access_workspace = workspaces_permission_check(self, workspace_id)
    if not access_workspace:
        raise AccessDeniedError(
            detail=f"Access denied to workspace-id - {workspace_id}"
        )
    is_file = check_is_file(self, sts_url, workspace_id, workspace_path)
    if not is_file:
        raise paramException(
            title="Param Error",
            detail="The given workspace path does not represent a file. Please try again.",
        )


def return_entity_type(data_source: str, cohort_info: json) -> str:
    """
    Function to return entity type based on the cohort info present in public assets
    """
    if data_source not in cohort_info:
        raise InvalidRepoException(data_source)
    for repo, dict in cohort_info.items():
        if data_source == repo:
            if dict["file_structure"] == "single":
                entity_type = "dataset"
            elif dict["file_structure"] == "multiple":
                entity_type = "sample"
    return entity_type


def get_files_in_dir(path_to_dir: str) -> list:
    """
    returns the files in a given directory

    Arguments:
        path_to_dir: str

    Returns:
        list of files in dir : list
    """
    directory = os.fsencode(path_to_dir)
    file_names = os.listdir(directory)
    return file_names


def parseInt(sin):
    """
    parsed the value passed as int  as done by js.
    python equivalent of js parseInt
    example:
        parseInt("100n")  = 100
        parseInt("400m")  = 400

    Arguments:
        sin -- value to be parsed as int

    Returns:
        int
    """
    m = re.search(r"^(\d+)[.,]?\d*?", str(sin))
    parsed_int = int(m.groups()[-1]) if m and not callable(sin) else None
    return parsed_int
