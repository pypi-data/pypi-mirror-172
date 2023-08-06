"""AWS specific settings."""

from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from censys.cloud_connectors.aws_connector.enums import AwsResourceTypes
from censys.cloud_connectors.common.enums import ProviderEnum
from censys.cloud_connectors.common.settings import ProviderSpecificSettings


class AwsAccountNumber(PositiveInt):
    """Account Number."""

    lt = 10**12


class AwsAccount(BaseModel):
    """AWS Account."""

    account_number: AwsAccountNumber = Field()
    access_key: Optional[str] = Field(min_length=1)
    secret_key: Optional[str] = Field(min_length=1)
    role_name: Optional[str] = Field(min_length=1)
    role_session_name: Optional[str] = Field(min_length=1)
    ignore_tags: Optional[list[str]] = Field(min_length=1)


class AwsSpecificSettings(ProviderSpecificSettings):
    """AWS specific settings."""

    provider = ProviderEnum.AWS
    ignore: Optional[list[AwsResourceTypes]] = None

    account_number: Optional[AwsAccountNumber] = Field()
    access_key: Optional[str] = Field(min_length=1)
    secret_key: Optional[str] = Field(min_length=1)
    role_name: Optional[str] = Field(min_length=1)
    role_session_name: Optional[str] = Field(min_length=1)
    ignore_tags: Optional[list[str]] = Field(min_length=1)

    session_token: Optional[str] = Field(min_length=1)
    external_id: Optional[str] = Field(min_length=1)

    accounts: Optional[list[AwsAccount]] = None

    regions: list[str] = Field(min_items=1)

    def get_provider_key(self) -> tuple:
        """Get provider key.

        Returns:
            tuple: [str, str]: Provider key.
        """
        accounts = []
        if self.accounts:
            for account in self.accounts:
                accounts.append(str(account.account_number))
        else:
            accounts.append(str(self.account_number))

        return ("_".join(sorted(accounts)), "_".join(self.regions))

    def get_provider_payload(self) -> dict:
        """Get the provider payload.

        Returns:
            dict: The provider payload.
        """
        return {
            self.provider: {
                "account_number": self.account_number,
            }
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a ProviderSpecificSettings object from a dictionary.

        Args:
            data (dict): The dictionary to use.

        Returns:
            ProviderSpecificSettings: The settings.
        """
        if provider_name := data.get("provider"):
            data["provider"] = provider_name.title()

        for index, account in enumerate(data.get("accounts") or []):
            data["accounts"][index] = AwsAccount(**account)

        return cls(**data)

    def get_credentials(self):
        """Generator for all configured credentials. Any values within the accounts block will take precedence over the overall values.

        Yields:
            dict[str, Any]
        """
        if self.accounts:
            for account in self.accounts:
                yield {
                    "account_number": (account.account_number or self.account_number),
                    "access_key": (account.access_key or self.access_key),
                    "secret_key": (account.secret_key or self.secret_key),
                    "role_name": (account.role_name or self.role_name),
                    "role_session_name": (
                        account.role_session_name or self.role_session_name
                    ),
                    # TODO: should this merge or override?
                    "ignore_tags": (account.ignore_tags or self.ignore_tags),
                }

        else:
            yield {
                "account_number": self.account_number,
                "access_key": self.access_key,
                "secret_key": self.secret_key,
                "role_name": self.role_name,
                "role_session_name": self.role_session_name,
                "ignore_tags": self.ignore_tags,
            }
