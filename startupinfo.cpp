#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// Extract a string value from simple JSON using only std::string
string getValueFromJson(const string& json, const string& key) {
    string pattern = "\"" + key + "\"";
    size_t keyPos = json.find(pattern);
    if (keyPos == string::npos) return "";

    size_t colonPos = json.find(":", keyPos);
    if (colonPos == string::npos) return "";

    size_t quoteStart = json.find("\"", colonPos + 1);
    if (quoteStart == string::npos) return "";

    size_t quoteEnd = json.find("\"", quoteStart + 1);
    if (quoteEnd == string::npos) return "";

    return json.substr(quoteStart + 1, quoteEnd - quoteStart - 1);
}

int main() {
    // Read info.json into a string
    ifstream file("info.json");
    if (!file.is_open()) {
        cout << "Could not open info.json\n";
        return 1;
    }

    string json((istreambuf_iterator<char>(file)),
                istreambuf_iterator<char>());

    // Extract all fields
    string version = getValueFromJson(json, "version");
    string name    = getValueFromJson(json, "name");
    string ide     = getValueFromJson(json, "ide");
    string engine  = getValueFromJson(json, "engine");

    // Apply defaults if missing
    if (version.empty()) version = "Unknown";
    if (name.empty())    name    = "Unknown App";
    if (ide.empty())     ide     = "Unknown IDE";
    if (engine.empty())  engine  = "Unknown Engine";

    // Output
    cout << name << " " << version << " initialising..." << endl;
    cout << "Engine: " << engine << endl;
    cout << "Development IDE: " << ide << endl;
    cout << "This project is made by volunteers. Please don’t steal our code!" << endl;

    return 0;
}