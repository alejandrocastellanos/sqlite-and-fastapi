export $(cat .env | sed -e /^$/d -e /^#/d | xargs -0)

uvicorn main:app --reload