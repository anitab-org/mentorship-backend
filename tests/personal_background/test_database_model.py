import unittest
from tests.base_test_case import BaseTestCase
from app.utils.bitschema_utils import (
    Gender,
    Age,
    Ethnicity,
    SexualOrientation,
    Religion,
    PhysicalAbility,
    MentalAbility,
    SocioEconomic,
    HighestEducation,
    YearsOfExperience,
)
from app.database.models.user import UserModel
from app.database.models.personal_background import PersonalBackgroundModel
from app.database.sqlalchemy_extension import db
from app.database.db_types.JsonCustomType import JsonCustomType
from tests.test_data import user1

# Testing User's Personal background database model
class TestPersonalBackgroundModel(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Add a user into the database
        user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )

        db.session.add(user)
        db.session.commit()

        self.user = UserModel.query.filter_by(email=user.email).first()

    def test_user_background_not_exist(self):

        user_background = PersonalBackgroundModel.query.filter_by(
            user_id=self.user.id
        ).first()
        self.assertTrue(user_background is None)

    def test_user_background_successfully_added(self):
        # add user personal_background
        user_background = PersonalBackgroundModel(
            user_id=self.user.id,
            gender=Gender.FEMALE,
            age=Age.AGE_25_TO_34,
            ethnicity=Ethnicity.CAUCASIAN,
            sexual_orientation=SexualOrientation.LGBTQIA,
            religion=Religion.OTHER,
            physical_ability=PhysicalAbility.WITHOUT_DISABILITY,
            mental_ability=MentalAbility.WITHOUT_DISORDER,
            socio_economic=SocioEconomic.LOWER_MIDDLE,
            highest_education=HighestEducation.BACHELOR,
            years_of_experience=YearsOfExperience.UP_TO_10,
        )
        user_background.others = {"religion": "Daoism"}
        user_background.is_public = True

        db.session.add(user_background)
        db.session.commit()

        background = PersonalBackgroundModel.query.filter_by(
            user_id=self.user.id
        ).first()
        self.assertTrue(background is not None)
        self.assertTrue(background.id is not None)
        self.assertTrue(background.gender == user_background.gender)
        self.assertTrue(background.age == user_background.age)
        self.assertTrue(background.ethnicity == user_background.ethnicity)
        self.assertTrue(
            background.sexual_orientation == user_background.sexual_orientation
        )
        self.assertTrue(background.religion == user_background.religion)
        self.assertTrue(background.physical_ability == user_background.physical_ability)
        self.assertTrue(background.mental_ability == user_background.mental_ability)
        self.assertTrue(background.socio_economic == user_background.socio_economic)
        self.assertTrue(
            background.highest_education == user_background.highest_education
        )
        self.assertTrue(
            background.years_of_experience == user_background.years_of_experience
        )
        self.assertTrue(background.others == user_background.others)
        self.assertTrue(background.is_public == user_background.is_public)


if __name__ == "__main__":
    unittest.main()
