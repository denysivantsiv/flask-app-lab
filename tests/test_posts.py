import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post("/post/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "is_active": "y",
                "publish_date": "2026-11-24T12:00",
                "category": "tech"
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)
            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)

    def test_list_posts(self):
        with self.app.app_context():
            p = Post(title="Visible Post", content="Content text", is_active=True)
            db.session.add(p)
            db.session.commit()
            response = self.client.get("/post/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Visible Post", response.data)

    def test_view_post_detail(self):
        with self.app.app_context():
            p = Post(title="Detail Post", content="Detailed content")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail Post", response.data)

    def test_update_post(self):
        with self.app.app_context():
            p = Post(title="Old Title", content="Old Content")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.post(f"/post/{post_id}/update", data={
            "title": "Updated Title",
            "content": "Updated Content",
            "is_active": "y",
            "publish_date": "2026-11-24T13:00",
            "category": "news"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Title", response.data)

    def test_delete_post(self):
        with self.app.app_context():
            p = Post(title="To Delete", content="Delete me")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        check = self.client.get(f"/post/{post_id}")
        self.assertEqual(check.status_code, 404)

    def test_404_not_found(self):
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()