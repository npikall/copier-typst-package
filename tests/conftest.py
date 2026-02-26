from typing import Literal

from pydantic import BaseModel

type CopyrightLicenseOptions = Literal["Apache-2.0", "MIT", "Unlicense", "None"]


class BaseUserAnswers(BaseModel):
    project: str = "foobar"
    git_user: str = "jdoe"
    git_email: str = "john.doe@email.com"


class FullUserAnswers(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions = "MIT"


class ChooseLicense(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions
