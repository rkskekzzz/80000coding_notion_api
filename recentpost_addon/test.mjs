import fetch from 'node-fetch';


async function fetchData() {
  const response = await fetch("https://api.notion.com/v1/databases/94e689f5b19947b1ab0f9b5f2d52962b/query",
    {
      method: 'POST',
      headers: {
	"Authorization": "Bearer secret_9NO3Q5X284CSDNElevo2rcKOCXnlDBPn3WwJFqOYrWs",
	"Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json"
      },
    }
  );
  const result = await response.text();
  const result_json = JSON.parse(result);
  const posts = result_json.results.slice(0,6);

  for (let i = 0 ; i < posts.length ; ++i) {
    if (posts[i].cover) console.log(posts[i].cover.external.url);
    console.log(posts[i].properties['제목']['title'][0]['plain_text']);
    console.log(posts[i].properties['rich_text']['formula']['string']);	  
  }
}

fetchData();
