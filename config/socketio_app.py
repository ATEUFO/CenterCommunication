import socketio
import os

# Initialize Socket.IO AsyncServer
# We keep this file as simple as possible to avoid circular imports
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")
    await sio.emit('connection_success', {'sid': sid}, room=sid)

@sio.event
async def join_post(sid, data):
    post_id = data.get('post_id')
    if post_id:
        room = f"post_{post_id}"
        await sio.enter_room(sid, room)
        print(f"Client {sid} joined room {room}")

@sio.event
async def leave_post(sid, data):
    post_id = data.get('post_id')
    if post_id:
        room = f"post_{post_id}"
        await sio.leave_room(sid, room)
        print(f"Client {sid} left room {room}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

def emit_new_comment(comment):
    """
    Synchronous helper to emit new comment to the correct room.
    """
    from apps.comments.serializers import CommentSerializer
    import asyncio
    
    # Define a helper that runs in the event loop
    async def _emit():
        serializer = CommentSerializer(comment)
        data = serializer.data
        room = f"post_{comment.post.id}"
        await sio.emit('new_comment', data, room=room)

    # Trigger the async emission
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(_emit(), loop)
        else:
            asyncio.run(_emit())
    except Exception as e:
        # In some contexts (like management commands), no loop exists
        print(f"Socket.IO emission failed: {e}")
