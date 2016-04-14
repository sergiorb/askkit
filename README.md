# Askkit
A polling system made with Django - **development branch**

#### TODO:

Poll and Option model save methods should **NOT** update its last modification
field when update "total_votes" and "vote_quantity" (on */polls/models.py*)

use select_related() (on */api/serializers_polls.py*)

move from generic.View to rest_framework.View ?? (on */api/views_celery.py*)

~~If request.user == owner~~ or in_list(), retrieve object (on */api/views_polls.py*)

Add signup and close account methods (on */api/views_users.py*)

**Improve vote count trigger system** (on */polls/signals.py*)
