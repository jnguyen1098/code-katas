class Codec:

    def __init__(self):
        self.IDs = {}
        self.websites = {}
        self.key = 0
    
    def encode(self, longUrl: str) -> str:
        """Encodes a URL to a shortened URL.
        """
        tmp_rep = "http://tinyurl.com/" + str(self.key)
        self.IDs[longUrl] = tmp_rep
        self.websites[tmp_rep] = longUrl
        self.key += 1
        return tmp_rep

    def decode(self, shortUrl: str) -> str:
        """Decodes a shortened URL to its original URL.
        """
        return self.websites[shortUrl]

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(url))
