from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_developers():
    response = client.get("/developers")
    assert response.status_code == 200
    
def test_get_developer():
    response = client.get("/developers/677c7e283d1731563ba108c9")
    assert response.status_code == 200
    
def test_get_skills():
    response = client.get("/developers/677c7e283d1731563ba108c9/skills")
    assert response.status_code == 200
    
def test_get_experience():
    response = client.get("/developers/677c7e283d1731563ba108c9/experience")
    assert response.status_code == 200
    
def test_get_languages():
    response = client.get("/developers/677c7e283d1731563ba108c9/languages")
    assert response.status_code == 200
    
def test_create_developer():
    response = client.post("/developers", json={
        "name":"Pedro",
        "age":45,
        "country":"Mexico",
        "experience": [
            {
            "title": "Python Developer",
            "location": "Mexico",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "organization": "Google"
            }
        ],
        "skills": [
            {
            "name": "Python",
            "years": 5
            },
            {
            "name": "JavaScript",
            "years": 6
            },
            {
            "name": "React",
            "years": 2
            }
        ],
        "languages": [
            {
            "name": "Spanish",
            "level": "Native"
            },
            {
            "name": "English",
            "level": "Intermediate"
            }
        ]
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Developer created"}
    
def test_update_developer():
    response = client.put("/developers/677c7e283d1731563ba108c9", json={
        "name":"Pedro",
        "age":45,
        "country":"Mexico",
        "experience": [
            {
            "title": "Python Developer",
            "location": "Mexico",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "organization": "Google"
            }
        ],
        "skills": [
            {
            "name": "Python",
            "years": 5
            },
            {
            "name": "JavaScript",
            "years": 6
            },
            {
            "name": "React",
            "years": 2
            }
        ],
        "languages": [
            {
            "name": "Spanish",
            "level": "Native"
            },
            {
            "name": "English",
            "level": "Intermediate"
            }
        ]
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Developer updated"}
    
def test_update_developer_not_found():
    response = client.put("/developers/677c7e283d1731563ba108c8", json={
        "name":"Pedro",
        "age":45,
        "country":"Mexico",
        "experience": [
            {
            "title": "Python Developer",
            "location": "Mexico",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "organization": "Google"
            }
        ],
        "skills": [
            {
            "name": "Python",
            "years": 5
            },
            {
            "name": "JavaScript",
            "years": 6
            },
            {
            "name": "React",
            "years": 2
            }
        ],
        "languages": [
            {
            "name": "Spanish",
            "level": "Native"
            },
            {
            "name": "English",
            "level": "Intermediate"
            }
        ]
    })
    assert response.status_code == 404
    assert response.json() == {"message": "Developer not found"}
    
def test_delete_developer():
    response = client.delete("/developers/677c7e283d1731563ba108c9")
    assert response.status_code == 200