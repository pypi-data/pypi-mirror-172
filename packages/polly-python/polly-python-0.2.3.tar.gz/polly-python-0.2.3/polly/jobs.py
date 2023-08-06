from multiprocessing import AuthenticationError
import re
from polly import helpers
from polly.auth import Polly
from polly.errors import (
    InvalidParameterException,
    InvalidPathException,
    UnauthorizedException,
    InvalidJobFunctionParameterException,
    extract_json_api_error,
)
from polly.helpers import (
    get_user_details,
    parseInt,
)

# from polly.constants import MIN_REQUIRED_KEYS_FOR_JOBS, MACHINES_FOR_JOBS
from polly.constants import COMPUTE_ENV_VARIABLE
import polly.http_response_codes as http_codes
from polly import constants as const

import pandas as pd
import os
import json


class jobs:
    """
    The polly_jobs class contains functions which can be used to create, cancel and monitor polly jobs,

    ``Args:``
        |  ``token (str):`` token copy from polly.

    .. code::


            from polly.jobs import jobs
            # To use this class initialize a object like this if you are not authorised on polly
            jobs = jobs(token)

    If you are authorised then you can initialize object without token to know about :ref:`authentication <auth>`.
    """

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
    ) -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"

    # project_id -> workspace_id
    # job_file -> json file
    def submit_job(self, project_id: str, job_file: str) -> pd.DataFrame:
        """
        submits  a polly cli job in the given workspace

        Args:
            project_id (str) :  workspace id : str
            job_file (str) : required configuration json file path : str

        Returns:
            on success: dataframe with workspace id and job id
            failure: throw errors
        """
        parameter_check_dict = {}
        parameter_check_dict["project_id"] = project_id
        parameter_check_dict["job_file"] = job_file
        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        try:
            with open(job_file, "r") as jobfile:
                jobData = json.load(jobfile)
                # self._validate_job_json(jobData)
        except Exception as err:
            raise err

        # TODO: add file validation for json
        jobData = self._add_secret_env_keys_to_jobData(jobData, project_id)
        # print("** added secret env variables *** Job data looks like this: ")
        # print(jobData)
        job_post_data = self._submit_job_to_polly(project_id, jobData)
        # print(job_post_data)
        submitted_job_id = job_post_data.json().get("data").get("job_id")
        project_id = job_post_data.json().get("data").get("project_id")
        submittedProject = {"Workspace ID": project_id, "Job ID": submitted_job_id}
        submittedProject_df = pd.DataFrame([submittedProject])
        return submittedProject_df

    def cancel_job(self, project_id: str, job_id: str):
        """
        cancel a polly job.

        Args:
            project_id (str) : workspace id : str
            job_id (str) : job id

        Raises:
            InvalidParameterException
            err:
        """
        parameter_check_dict = {}
        parameter_check_dict["project_id"] = project_id
        parameter_check_dict["job_id"] = job_id
        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs/{job_id}"
        try:
            job_data = {}
            job_data = self._add_secret_env_keys_to_jobData(
                jobData=job_data, project_id=project_id
            )
            self._get_headers_for_job(job_data)
            # successfull -> returns 204
            postData = self.session.delete(self.jobUrl)
            if postData.status_code == 204:
                print("Cancelled job ID " + job_id + " successfully!")
            else:
                # handling this differently because postData.text is a str
                if postData.text:
                    postData_resp_json = json.loads(postData.text)
                else:
                    postData_resp_json = postData.json()
                error = postData_resp_json.get("error")
                if error is None:
                    error = postData_resp_json.get("errors", [])[0]
                if "detail" in error:
                    detail = error.get("detail", "")
                    print("Failed to cancel the job.: " + detail)
                else:
                    print("Failed to cancel the job.")
        except Exception as err:
            print("Failed to cancel the job.")
            raise err

    def job_status(self, project_id: str, job_id="", internalCalls=False) -> dict:
        """
        Get the status of a job given the rproject id and job id.
        if no job id give, gives status for all the jobs in the
        provided workspace

        Arguments:
            project_id (str) -- workspace id
            job_id (str) --  job id

        Keyword Arguments:
            internalCalls -- _description_ (default: {False})

        Returns:
            dataframe with job id, job name and status sorted as per created
            timestamp
        """
        parameter_check_dict = {}
        parameter_check_dict["project_id"] = project_id
        if job_id:
            parameter_check_dict["job_id"] = job_id
        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        sortedJobsTemp = None
        sortedJobs = []
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs/{job_id}"

        # TODO: Yogesh : from a job id if we can get the project id. -> improvement
        # TODO: job id can be a optional parameter -> MVP
        jobData = {}
        try:
            updated_jobData = self._add_secret_env_keys_to_jobData(jobData, project_id)
            self._get_headers_for_job(updated_jobData)
            postDatas = self._get_data_for_job_id(self.jobUrl)
            if postDatas.status_code != const.OK:
                self._handle_response_errors(postDatas)
            # list of data
            else:
                sortedJobsTemp = postDatas.json()
                sortedJobs.extend(sortedJobsTemp.get("data"))
                for i in range(len(sortedJobsTemp.get("data"))):
                    if sortedJobsTemp.get("links", "") and sortedJobsTemp.get(
                        "links", ""
                    ).get("next", ""):
                        jobUrl = f"{self.base_url}{sortedJobsTemp.json().get('links').get('next')}"
                        postDatas = self._get_data_for_job_id(self, jobUrl)
                        if postDatas.status_code != const.OK:
                            self._handle_response_errors(postDatas)
                        sortedJobsTemp = postDatas.json()
                        sortedJobs.extend(sortedJobsTemp.get("data"))
                    else:
                        continue
        except Exception as err:
            print("Not able to get the status of the Job(s)")
            raise err
        sortedJobs = sorted(sortedJobs, key=lambda d: d["attributes"]["created_ts"])
        if internalCalls:
            return sortedJobs
        status_result_df = self._generate_job_status_df(sortedJobs)
        # with pd.option_context(
        #     "display.max_rows", 800, "display.max_columns", 800, "display.width", 1200
        # ):
        #     print(status_result_df)
        return status_result_df

    def _is_valid_job_id(self, project_id: str, job_id: str):
        """
        checks if the job id provided is valid
        checks the jobid in the jobs in the workspace

        Arguments:
            project_id (int or str) -- workspace id
            job_id (str) -- job id

        Returns:
            valid (bool) -- True if job id is valid
        """
        valid = False
        try:
            jobs_list = self.job_status(project_id, internalCalls=True)
            job_id_list = []
            for jobs in jobs_list:
                job_id_list.append(jobs.get("attributes").get("job_id"))
            if job_id in job_id_list:
                valid = True
        except Exception as err:
            raise err
        return valid

    def _handle_response_errors(self, postDatas):
        """
        api to handle the response errors

        Arguments:
            postDatas (json) : api response json

        """
        if postDatas.status_code == http_codes.FORBIDDEN:
            raise AuthenticationError("User access is denied. Please contact admin")
        elif postDatas.status_code == http_codes.UNAUTHORIZED:
            raise UnauthorizedException("User is unauthorized to access this")
        elif postDatas.status_code == http_codes.NOT_FOUND:
            error_title, error_detail = extract_json_api_error(postDatas.text)
            raise Exception(error_detail)
        else:
            error_title, error_detail = extract_json_api_error(postDatas.text)
            raise Exception(error_detail)

    def _generate_job_status_df(self, sortedJobs):
        """
        given a list of jobs related info dict this generates a dataframe of the job id, name and status

        Arguments:
            sortedJobs (list): list of job information

        Returns:
            status_result_df (pd.dataframe): dataframe containing job id, name
        """
        job_info_list = []
        if sortedJobs:
            for jobs in sortedJobs:
                job_info = {}
                job_info["id"] = jobs.get("attributes").get("job_id")
                job_info["name"] = jobs.get("attributes").get("job_name")
                job_info["job_state"] = jobs.get("attributes").get("state")
                job_info_list.append(job_info)
            status_result_df = pd.DataFrame(job_info_list)
            status_result_df.columns = ["Job ID", "Job Name", "Job State"]
        else:
            status_result_df = pd.DataFrame(columns=["Job ID", "Job Name", "Job State"])
        return status_result_df

    def _get_data_for_job_id(self, jobUrl):
        """
        given a url, gets the response for the url.
        """
        try:
            self.jobUrl = jobUrl
            if jobUrl:
                postDatas = self.session.get(self.jobUrl)
            else:
                postDatas = self.session.get(self.jobUrl)
        except Exception as err:
            raise err
        return postDatas

    def _add_secret_env_keys_to_jobData(self, jobData: json, project_id: str) -> json:
        """
        add env variables and values to the job data json needed for job run

        Args:
            jobData (json) :  json containing existing variables
            project_id (str):  workspace id

        Returns:
           appended job data json with the secret env variables
        """
        dict_secret_env_variables = self._get_secret_env_variables()
        if "secret_env" not in jobData:
            jobData["secret_env"] = {}
        jobData["secret_env"]["POLLY_REFRESH_TOKEN"] = dict_secret_env_variables.get(
            "refreshToken"
        )
        jobData["secret_env"]["POLLY_ID_TOKEN"] = dict_secret_env_variables.get(
            "idToken"
        )
        jobData["secret_env"]["POLLY_WORKSPACE_ID"] = project_id
        jobData["secret_env"]["POLLY_USER"] = dict_secret_env_variables.get("email")
        jobData["secret_env"]["POLLY_SUB"] = dict_secret_env_variables.get("sub")
        jobData["secret_env"]["POLLY_EXP"] = dict_secret_env_variables.get("exp")
        jobData["secret_env"]["POLLY_AUD"] = dict_secret_env_variables.get("aud")

        return jobData

    def _submit_job_to_polly(self, project_id: str, job_data: json):
        """
        given a complete job data and workspace id
        calling the api to start a job

        Args:
            project_id (str) : workspace id
            job_data (jsob) : json containing all required variables

        Raises:
            err

        Returns:
            response from the api call
        """
        submitBody = {"data": {"type": "jobs", "attributes": job_data}}

        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs"

        self._get_headers_for_job(job_data)
        try:
            postData = self.session.post(self.jobUrl, data=json.dumps(submitBody))
            # print(postData)
            # print(postData.json())
            error = postData.json().get("error")
            if error is not None:
                error = postData.json().get("errors")[0]
                if "title" in error:
                    title = error.get("title")
                    print(title)
                if "detail" in error:
                    detail = error.get("detail")
                    print(detail)
        except Exception as err:
            print("Not able to submit job")
            raise err
        return postData

    def _get_headers_for_job(self, job_data: json):
        """
        adds required headers for polly job api request
        in the session headers itself

        Arguments:
            job_data (json): json
        """
        # print("**** in get headers for job.. adding cookie for job..")
        self.session.headers["Cookie"] = helpers.makeRequestCookieForPollyJob(job_data)

    """
    def _validate_job_json(self, jobData: json):
        # first check for if it is valid json format is done as part of json.load()
        # second check for // checking if necessary fiels are present
        min_required_feilds = MIN_REQUIRED_KEYS_FOR_JOBS
        # find the min_required_feilds missing from jobdata
        diff_req_keys = []
        for req_key in min_required_feilds:
            if req_key not in jobData.keys():
                diff_req_keys.append(req_key)
        if len(diff_req_keys) > 0:
            if not (
                ((not ("cpu" in diff_req_keys)) and not ("memory" in diff_req_keys))
                or not ("machineType" in diff_req_keys)
            ):
                raise InvalidParameterException(
                    "Please mention either cpu and memory or machine type in the .json file"
                )

            if "cpu" in diff_req_keys:
                diff_req_keys.remove("cpu")
            if "memory" in diff_req_keys:
                diff_req_keys.remove("memory")
            if "machineType" in diff_req_keys:
                diff_req_keys.remove("machineType")
            if len(diff_req_keys) > 0:
                raise InvalidParameterException(
                    "Following entry(s) are missing in the discription file: "
                    + ",".join(diff_req_keys)
                )
            if "machineType" in jobData.keys():
                resourceTypes = MACHINES_FOR_JOBS
                if jobData.get("machineType") not in resourceTypes.keys():
                    print("invalid machine type")
                    #TODO: handle this error and throw error message accordingly.
            if "cpu" in jobData.keys():
                if not self._valid_cpu(jobData["cpu"]):
                    raise InvalidParameterException(
                        "CPU given is not valid. Please check the documantation for more information."
                    )
                if (
                    self._convert_cpu(jobData.cpu) > 2
                    and "machineType" not in jobData.keys()
                ):
                    print(
                        "Job seems to need more resources. Please use machine type to specify resources. "
                    )
                    #TODO: handle this and throw error message accordingly.
        return
    """

    def _valid_cpu(self, cpu: str) -> bool:
        matches = False
        cpu_regex = "^([+-]?[0-9.]+)([m]*[-+]?[0-9]*)$"
        match = re.fullmatch(cpu_regex, cpu)
        if match is not None:
            matches = True
        return matches

    def _convert_cpu(self, cpu: str):
        cpuRegex = "^[0-9]+m$"
        if re.fullmatch(cpuRegex, cpu):
            cpu_parsed = parseInt(cpu[0:-1]) * 0.001
            return cpu_parsed
        else:
            return parseInt(cpu)

    def _get_secret_env_variables(self) -> dict:
        # print("*** in get secret env variables.. ***")
        dict_secret_env_variables = {}
        user_details = get_user_details(self)
        # print("********** CALLING helpers.get_user_details_using_aws_cognito(self).....")
        user_details_aws_cognito = helpers.get_user_details_using_aws_cognito(self)
        dict_secret_env_variables["id"] = user_details.get("id")
        dict_secret_env_variables["type"] = user_details.get("type")
        dict_secret_env_variables["user_id"] = user_details.get("user_id")
        dict_secret_env_variables["email"] = user_details.get("email")
        dict_secret_env_variables["first_name"] = user_details.get("first_name")
        dict_secret_env_variables["last_name"] = user_details.get("last_name")
        dict_secret_env_variables["active"] = user_details.get("last_name")
        dict_secret_env_variables["created_at"] = user_details.get("created_at")
        dict_secret_env_variables["organizations"] = user_details.get("organizations")
        dict_secret_env_variables["sub"] = user_details_aws_cognito.get("sub")
        dict_secret_env_variables["exp"] = user_details_aws_cognito.get("exp")
        dict_secret_env_variables["refreshToken"] = user_details_aws_cognito.get(
            "refresh_token"
        )
        dict_secret_env_variables["idToken"] = user_details_aws_cognito.get("id_token")
        dict_secret_env_variables["attributes"] = user_details
        dict_secret_env_variables["aud"] = user_details_aws_cognito.get("aud")

        return dict_secret_env_variables

    def _parameter_check_for_jobs(self, paramter_dict: dict):
        for keys, values in paramter_dict.items():
            if keys == "project_id":
                project_id = values
                if not (
                    project_id
                    and (isinstance(project_id, str) or isinstance(project_id, int))
                ):
                    raise InvalidParameterException("project id/workspace id")
            if keys == "job_file":
                job_file = values
                if not (job_file):
                    raise InvalidParameterException("job_file")
                if not os.path.exists(job_file):
                    raise InvalidPathException(job_file)
            if keys == "job_id":
                job_id = values
                if not (job_id and (isinstance(job_id, str))):
                    raise InvalidParameterException(
                        "Missing/invalid datatype for job id"
                    )

                if not self._is_valid_job_id(project_id, job_id):
                    raise InvalidJobFunctionParameterException("Job id")
