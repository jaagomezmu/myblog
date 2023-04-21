from datetime import datetime, timedelta

import pytest
from blog.models import BlogPost, Comment, UserTag
from django.contrib.auth.models import User
from django.db.utils import DataError
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def user_1(db):
    user = User.objects.create_user("test_user")
    return user

@pytest.fixture
def user_2(db):
    user = User.objects.create_user("test_comment_user")
    return user

@pytest.fixture
def post_1(db, user_1):
    post = BlogPost.objects.create(title = 'test1',
                                   body = 'This is the body of the first test',
                                   author = user_1)
    return post

@pytest.fixture
def tagged_post(user_1, user_2):
    post = BlogPost.objects.create(title = 'Tagged Post', 
                                   body = 'Test body', 
                                   author = user_1)
    UserTag.objects.create(blogpost = post, user = user_1)
    UserTag.objects.create(blogpost = post, user = user_2)
    return post

@pytest.fixture
def old_tagged_post(user_1, user_2):
    post = BlogPost.objects.create(title = 'Old Tagged Post',
                                   body = 'Test body',
                                   author = user_1)
    UserTag.objects.create(blogpost = post, user = user_1, 
                           created_at = datetime.now()-timedelta(days = 15))
    UserTag.objects.create(blogpost = post, user = user_2, 
                           created_at = datetime.now()-timedelta(days = 3))
    return post

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
    
@pytest.mark.usefixtures("user_1")
class TestApiBlogPost:
    """To test the api endpoint 
    """
    pytestmark = pytest.mark.django_db
    
    def test_blogpost_api(self, user_1):
        
        url = reverse('post-list')
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        
        client.force_authenticate(user=user_1)
        
        # Api GET
        response = client.get(url,format = 'json')
                
        # Check response code
        assert response.status_code == 200
        
        # Check db
        assert BlogPost.objects.count() == 0 ; # Must be 0
        
        # Create a post
        post = BlogPost.objects.create(title = 'test1',
                                    body = 'This is the body of the first test',
                                    author = user_1)
        assert BlogPost.objects.count() == 1
        
        # Now. validate the api get again
        response = client.get(url,format = 'json')
        assert response.data['count'] == BlogPost.objects.count()
        
    def test_post_blogpost_api(self, user_1):
        
        url = reverse('post-list')
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        
        client.force_authenticate(user=user_1)
        
        # Check db
        assert BlogPost.objects.count() == 0 ; # Must be 0
        
        # Create a post without user
        response = client.post(url,
                               data={'body': 'Test_body',
                                     'title':'Test_Title'})
        # Check response code
        assert response.status_code == 201
        
        # Check db
        assert BlogPost.objects.count() == 1 ; # Must be 1
    
@pytest.mark.usefixtures("user_1")
class TestDetailViewSet:
    """To test the detail api endpoint
    """    
    pytestmark = pytest.mark.django_db
    
    def test_get(self, user_1):
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        client.force_authenticate(user=user_1)
        
        # Create a post
        post_test = BlogPost.objects.create(title='Test Post',
                                            body='Test Content',
                                            author=user_1)
        # Set url
        url = reverse('post-detail', args=[post_test.id])
        
        # Check response code
        response = client.get(url, format = 'json')    
        assert response.status_code == 200

        # Check title 
        assert response.data['title'] == 'Test Post'

    def test_patch(self, user_1):
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        client.force_authenticate(user=user_1)
        
        # Create a post
        post_test = BlogPost.objects.create(title='Test Post',
                                            body='Test Content',
                                            author=user_1)
        # Set url
        url = reverse('post-detail', args=[post_test.id])
               
        data = {'title': 'Updated Title'}
        
        # Check response code
        response = client.patch(url, data)  
        assert response.status_code == 200

        # Check title 
        assert response.data['title'] == 'Updated Title'

    def test_delete(self, user_1):
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        client.force_authenticate(user=user_1)
        
        # Create a post
        post_test = BlogPost.objects.create(title='Test Post',
                                            body='Test Content',
                                            author=user_1)
        # Set url
        url = reverse('post-detail', args=[post_test.id])
        
        # Check response code
        response = client.delete(url)  
        assert response.status_code == 204
        
        # Check db
        assert BlogPost.objects.count() == 0 ; # Must be 0

@pytest.mark.usefixtures("post_1", "user_1")
class TestCommentsModel:
    pytestmark = pytest.mark.django_db
    body = 'x'*255
    
    def test_creation_comment_with_user(self, post_1, user_1):
        # Create a comment with a user
        self.comment = Comment.objects.create(body = 'This is the body of the comment',
                                              blogpost = post_1,
                                              user = user_1)
        assert Comment.objects.count() == 1
        
    def test_creation_comment_without_user(self, post_1, user_1):    
        # Create a comment without a user
        self.comment = Comment.objects.create(body = 'This is the body of the comment',
                                              blogpost = post_1,
                                              user = None)
        assert Comment.objects.count() == 1
    
    def test_comment_body(self, post_1):
        # Create a body comment longer than 255 characters
        with pytest.raises(DataError):
            self.comment = Comment.objects.create(body = self.body + 'yyy',
                                                    blogpost = post_1,
                                                    user = None)
    
    def test_comment_blogpost(self, post_1):
        # Create a comment without a relation with the blogpost
        with pytest.raises(ValueError):
            self.comment = Comment.objects.create(body = self.body,
                                                    blogpost = 1,
                                                    user = None)
        # Create a comment with a relation with the blogpost
        self.comment = Comment.objects.create(body = self.body,
                                                    blogpost = post_1,
                                                    user = None)
        assert Comment.objects.count() == 1

@pytest.mark.usefixtures("user_1", "post_1", "user_2")
class TestCommentViewSet:
    """To test the comment api endpoint
    """    
    pytestmark = pytest.mark.django_db
    
    def test_get(self, user_1, post_1):
        
        # Login
        client = APIClient()
        client.login(username=user_1.username, password=user_1.password)
        client.force_authenticate(user=user_1)
        
        # Create a comment
        comment_test = Comment.objects.create(body = 'Test Content',
                                              blogpost = post_1,
                                              user = None)
        # Set url
        url = reverse('comment-detail', args=[comment_test.id])
        
        # Check response code
        response = client.get(url, format = 'json')    
        assert response.status_code == 200

        # Check title 
        assert response.data['body'] == 'Test Content'
        
        # Check all comments
        url = reverse('comment-list')
        
        # Check response code
        response = client.get(url, format = 'json') 
        assert response.status_code == 200
        
        # Check db
        assert response.data['count'] == Comment.objects.count()

    def test_patch(self, user_2, post_1):
        
        # Login
        client = APIClient()
        client.login(username=user_2.username, password=user_2.password)
        client.force_authenticate(user=user_2)
        
        # Create a comment
        comment_test = Comment.objects.create(body = 'Test Content',
                                              blogpost = post_1,
                                              user = user_2)
        # Set url
        url = reverse('comment-detail', args=[comment_test.id])
               
        data = {'body': 'Updated body'}
        
        # Check response code
        response = client.patch(url, data)  
        assert response.status_code == 200

        # Check body
        assert response.data['body'] == 'Updated body'
        
        # Delete the user that creates the comment 
        User.objects.filter(id=user_2.id).delete()
        
        # Get the comments
        url2 = reverse('comment-list')
        response = client.get(url2)
        
        # Check response code in get list
        assert response.status_code == 200
        
        # Check the comment
        assert response.data['results'][0]['user'] == None
    
    def test_delete(self, user_2, post_1):
        
        # Login
        client = APIClient()
        client.login(username=user_2.username, password=user_2.password)
        client.force_authenticate(user=user_2)
        
        # Create a comment
        comment_test = Comment.objects.create(body = 'Test Content',
                                              blogpost = post_1,
                                              user = user_2)
        # Set url
        url = reverse('comment-detail', args=[comment_test.id])
        
        # Check response code in delete
        response = client.delete(url)  
        assert response.status_code == 204
        
        # Check db
        assert Comment.objects.count() == 0 ; # Must be 0

@pytest.mark.usefixtures("user_1", "post_1", "user_2")
class TestModelAndCommentModel:
    """To test the comment and blogpost model
    """    
    pytestmark = pytest.mark.django_db
    
    def test_comments_count(self, user_1):
        post_test = BlogPost.objects.create(title='Test Post',
                                            body='Test Content',
                                            author=user_1)
        Comment.objects.create(body = 'Body of the first comment',
                               blogpost = post_test,
                               user = user_1)
        Comment.objects.create(body = 'Body 2 of the first comment',
                               blogpost = post_test,
                               user = user_1)
        assert post_test.comments_count == 2

@pytest.mark.usefixtures("user_1", "post_1", "tagged_post")
class TestPropertiesBlogPost:
    """To test the blogpost properties
    """    
    pytestmark = pytest.mark.django_db
    
    def test_tagged_count(self, post_1, tagged_post):

        assert post_1.tagged_count == 0
        assert tagged_post.tagged_count == 2
    
    def test_last_tag_date(self, post_1, tagged_post, old_tagged_post):
        assert post_1.last_tag_date is None
        assert tagged_post.last_tag_date == max(tag.created_at for tag in tagged_post.usertags.all())
        assert old_tagged_post.last_tag_date == max(tag.created_at for tag in old_tagged_post.usertags.all())
