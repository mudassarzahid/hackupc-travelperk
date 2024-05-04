from muselsl import list_muses, stream

muses = list_muses()
print(muses)
stream(muses[0]["address"])

# Note: Streaming is synchronous, so code here will not execute until after the stream has been closed
print("Stream has ended")
