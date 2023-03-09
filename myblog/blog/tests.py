import pytest
from blog.models import BlogPost
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def user_1(db):
    user = User.objects.create_user("test_user")
    return user

@pytest.mark.usefixtures("user_1")
class TestPostModel:
    pytestmark = pytest.mark.django_db

    length = 1
    author = ''
    title = 'x'*100

    def test_creation_blog_post_in_postgres(self, user_1):
        self.post = BlogPost.objects.create(title = 'test1',
                                    body = 'This is the body of the first test',
                                    author = user_1)
        assert BlogPost.objects.count() == self.length

    def test_foreign_key_in_blog_post_model(self, user_1):
        with pytest.raises(ValueError) as exc_value:
            post = BlogPost.objects.create(title = 'test2',
                                           body = 'This is the body of the second test',
                                        #    author = user_1,
                                           author = self.author,
                                            )
    def test_display_name_of_blog_post_model(self, user_1):
        post = BlogPost.objects.create(title = self.title,
                                       body = 'This is the body of the third test',
                                       author = user_1,
                                       )
        assert str(post) == self.title

@pytest.mark.usefixtures("user_1",)
class TestUserStory:
    """To test the Login/Logout/Register tasks
    """
    pytestmark = pytest.mark.django_db

    def test_register(self, client, user_1):
        # Post data in register
        response = client.post(reverse('register'), data={
            'username': user_1.username,
            'password1': user_1.password,
            'password2': user_1.password
        })
        # Check response code
        assert response.status_code == 200

        # Check db
        users = User.objects.count()
        assert users == 1

    def test_login(self, client, user_1):
        # Get login page
        response = client.get(reverse('login'))

        # Check response code
        assert response.status_code == 200

        # Check 'Log in' in response
        assert 'Login' in response.content.decode()

        # Log the user in
        user = user_1
        client.login(
            username = user.username,
            password = user.password
        )
        # Check response code
        response = client.get(reverse('index'))
        assert response.status_code == 200

    def test_logout(self, client, user_1):
        # Login
        user = user_1
        client.login(
            username = user.username,
            password = user.password
        )
        response = client.get(reverse('login'))
        # Check response code
        assert response.status_code == 200
        # Log out
        client.logout()
        # Check response code
        response = client.get(reverse('login'))
        assert response.status_code == 200
        # Check Log out not in content
        assert 'Log out' not in response.content.decode()
