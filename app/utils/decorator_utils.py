from app.database.models.user import UserModel


# definition of decorator to validate user
def user_validation(user_function):

    def validator(*args, **kwargs):

        #  check if the given paramenters are in form of dict (to get user_id)
        if kwargs:

            # if parameters are given in form of dict
            user = UserModel.find_by_id(kwargs['user_id'])

        else:

            # if parameters are given as args
            user = UserModel.find_by_id(args[0])

        # verify if user exists
        if user:

            # verify if user has verified his/her email
            if user.is_email_verified:
                return user_function(*args, **kwargs)

            else:
                return {'message': 'You have not confirmed your email.'}, 400

        else:
            return {'message': 'User does not exist.'}, 404

    return validator
