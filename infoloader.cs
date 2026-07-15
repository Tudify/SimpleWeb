using System;
using System.IO;

class infocheck
{
    static void Main()
    {
        string filePath = Path.Combine(AppContext.BaseDirectory, "info.json");
        string jsonContent =
@"{
    ""version"": ""5.0.0"",
    ""name"": ""Tudify SimpleWeb"",
    ""ide"": ""none"",
    ""engine"": ""SWE-Multiplatform"",
    ""font"": ""Hack""
}";
        if (!File.Exists(filePath))
        {
            File.WriteAllText(filePath, jsonContent);
            Console.WriteLine("info.json was created.");
        }
        else
        {
            Console.WriteLine("info.json already exists.");
        }
    }
}