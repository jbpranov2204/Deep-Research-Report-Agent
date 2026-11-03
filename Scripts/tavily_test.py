from tavily import TavilyClient
client = TavilyClient("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")
response = client.search(
    query="latest updates about google stocks",
    search_depth="advanced"
)
print(response)