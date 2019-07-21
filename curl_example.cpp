#include <iostream>
#include <string>
#include <curl/curl.h>
#include <vector>
#include <fmt/core.h>
#include <fmt/format.h>

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}


struct auth{

	std::string client_id, client_secret;
	auth(): client_id("e1f239ec0ee443689d6786fd3f397af1"), client_secret("cbecd4d200f8482d910cb1db77d6f10c"){}

};

class SpotInstance{
	public:

	private:
		std::vector<std::string> options {
			"albums"
		};
		std::string token = "meh";
		std::string base_url = "https://api.spotify.com/v1/";
		auth authentication;
};

int main(void)
{
	CURL *curl; // cURL class object in which we have access to loads of different methods
	CURLcode res; // result from the cURL response
	std::string read_buffer; // the buffer in which cURL stores the repsonse
	std::string url = "https://jsonplaceholder.typicode.com/todos/";
	std::string spot_url = "https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy/tracks?market=ES&limit=10&offset=5";
	curl = curl_easy_init(); // we now can use it
	if(curl) { // if the object now exists
		struct curl_slist* headers = nullptr;
		SpotInstance test;
		headers = curl_slist_append(headers, "Content-Type: application/json");
		headers = curl_slist_append(headers, "Authorization: Bearer BQDiSd9q-griLto-uyrpAS9vlg3OsnWwY3RhlfoyghvpAjIu4MMTQhsP7GrolmHz06rRz9OlmcjOdGOXvwd0ERWSzHxRMHmf4jABnACyrAYvVm46vkTrg-rvBubClY1zw8aIawqzZ2qKPyM1c6eyKAnhsxLcx9suB9uyi2MxYFDYT3Ga9-MscUyo1g_Eqt05cQ5JVfLanKKkt0aEWUL7YOLR6-JTt81Q3MyXwts2BWdLULa2PsZknK3XMwwrNx22oK_PqW6qqUtcwqv8dLKX");

		curl_easy_setopt(curl, CURLOPT_URL, spot_url.c_str()); // we pass in the url we want
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback); // a function needs to be passed in to handle the response given to the server
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &read_buffer); // pass in the buffer
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		res = curl_easy_perform(curl); // once all the different options have been tacked onto the curl object, we then act on those options
		curl_easy_cleanup(curl); // cleanup

		// std::cout << read_buffer << std::endl;
		fmt::print("Hello {}", "world");

	}
	else{
		std::cerr << "Something went wrong....cowardly refusing" << std::endl;
	}
	return 0;
}

