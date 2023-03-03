from blog.models import BlogPost
from django.contrib.auth.models import User
import pytest

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
    
    def test_creation_blog_post_1(self, user_1):
        self.post = BlogPost.objects.create(title = 'test1',
                                    body = 'This is the body of the first test',
                                    author = user_1)        
        assert BlogPost.objects.count() == self.length
    
    def test_creation_blog_post_2(self, user_1):
        with pytest.raises(ValueError) as exc_value:
            post = BlogPost.objects.create(title = 'test2',
                                           body = 'This is the body of the second test',
                                        #    author = user_1,
                                           author = self.author,
                                            )
    def test_creation_blog_post_3(self, user_1):
        post = BlogPost.objects.create(title = self.title,
                                       body = 'This is the body of the third test',
                                       author = user_1,
                                       )
        assert str(post) == self.title

        
            