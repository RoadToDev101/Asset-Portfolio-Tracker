from supertokens_python.recipe import (
    session,
    thirdpartyemailpassword,
    dashboard,
    userroles,
)
from supertokens_python.recipe.thirdparty.provider import (
    ProviderInput,
    ProviderConfig,
    ProviderClientConfig,
)
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)
import os
from dotenv import load_dotenv

load_dotenv()

# this is the location of the SuperTokens core.
supertokens_config = SupertokensConfig(
    # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
    connection_uri="http://localhost:3567",
    # api_key=<API_KEY(if configured)>
)

app_info = InputAppInfo(
    app_name="PortfolioTracker",
    api_domain="http://localhost:8000",
    website_domain="http://localhost:3000",
)

framework = "fastapi"

# recipeList contains all the modules that you want to
# use from SuperTokens. See the full list here: https://supertokens.com/docs/guides
recipe_list = [
    session.init(),
    thirdpartyemailpassword.init(
        providers=[
            ProviderInput(
                config=ProviderConfig(
                    third_party_id="google",
                    clients=[
                        ProviderClientConfig(
                            client_id="1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
                            client_secret="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",
                        ),
                    ],
                ),
            ),
            ProviderInput(
                config=ProviderConfig(
                    third_party_id="github",
                    clients=[
                        ProviderClientConfig(
                            client_id="467101b197249757c71f",
                            client_secret="e97051221f4b6426e8fe8d51486396703012f5bd",
                        ),
                    ],
                ),
            ),
            # ProviderInput(
            #     config=ProviderConfig(
            #         third_party_id="apple",
            #         clients=[
            #             ProviderClientConfig(
            #                 client_id="4398792-io.supertokens.example.service",
            #                 additional_config={
            #                     "keyId": "7M48Y4RYDL",
            #                     "privateKey": "-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgu8gXs+XYkqXD6Ala9Sf/iJXzhbwcoG5dMh1OonpdJUmgCgYIKoZIzj0DAQehRANCAASfrvlFbFCYqn3I2zeknYXLwtH30JuOKestDbSfZYxZNMqhF/OzdZFTV0zc5u5s3eN+oCWbnvl0hM+9IW0UlkdA\n-----END PRIVATE KEY-----",
            #                     "teamId": "YWQCXGJRJL",
            #                 },
            #             ),
            #         ],
            #     ),
            # ),
            # ProviderInput(
            #     config=ProviderConfig(
            #         third_party_id="twitter",
            #         clients=[
            #             ProviderClientConfig(
            #                 client_id='4398792-WXpqVXRiazdRMGNJdEZIa3RVQXc6MTpjaQ',
            #                 client_secret='BivMbtwmcygbRLNQ0zk45yxvW246tnYnTFFq-LH39NwZMxFpdC'
            #             ),
            #         ],
            #     ),
            # ),
        ]
    ),
    dashboard.init(
        admins=[
            os.getenv("SUPER_TOKENS_ADMIN_EMAIL"),
        ]
    ),
    userroles.init(),
]
