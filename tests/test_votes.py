import pytest
from app import models

#vote on someone else post
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

#vote on our own post
def test_vote_on_our_own_post(authorized_client, test_posts):
    #voting on our own vote # but we don't have limitation inside vote.py for voting on our vote#logic you can't vote on your own post
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

#CHAIN OF EVENTS 
#we call authorized_client and test_posts before it the test runs
#authorized_client calls client and token inside conftest.py file
#token calls test_user # test_user is called in test_posts as an owner #test_posts[3] is owned by test_user2 -> vote on others user post
#test_posts[0].id -> vote on post we have created
#client calls session
#session creates and drops db

#set one of our post to have a vote #import pytest first
@pytest.fixture()
def test_vote(test_posts, session, test_user): #session to change it in db directly # we need to import models
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

#what happens when user is trying to like a post that he is already liked
def test_vote_twice_post(authorized_client, test_posts, test_vote): #we need to have a post that was already voted on
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1}) #dir is one revote on hat vote
    assert res.status_code == 409

#delete vote if vote exists
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

#delete a vote that does not exists
def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404

#vote on post that does not exist
def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404

#user that is not authenticated can not vote
def test_vote_unathorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401


