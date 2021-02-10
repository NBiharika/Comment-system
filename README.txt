#API usage
**URL** '/insert_comment'
**METHOD** 'POST'

**URL** '/reply'
**METHOD** 'POST'

**URL** '/view_all'
**METHOD** 'GET'

# Success Response
**Condition**: If everything is OK
**Code** : '200'
**Content Example**
'''json
{
    "status": 200
}
'''

# Error Response
 **Condition**: if the username doesn't exist to reply or if the comment count is 0
 **Code**: 302
 
