from rest_framework import routers

from .views import TodoViewSet

router = routers.DefaultRouter()
# /api/todo/...
router.register(r'todo', TodoViewSet)

urlpatterns = router.urls

todo_list = TodoViewSet.as_view({
    'get': 'list',
    'post': 'create',
}) 

# REST

# GET  -> retrieve
# POST -> create
# DELETE -> destroy

# RPC

# GET
# getTodoItem()
# destroyItem()

# Web Sockets

# p2p

# Streaming
