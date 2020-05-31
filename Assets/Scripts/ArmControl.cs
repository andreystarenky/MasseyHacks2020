using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ArmControl : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {

        try
        {
            string path = "Assets/movement";

            //Read the text from directly from the test.txt file
            StreamReader reader = new StreamReader(path);

            string readValue = reader.ReadToEnd();

            string[] words = readValue.Split('\n');

            Debug.Log("1 is " + words[0]);
            Debug.Log("2 is " + words[1]);

            reader.Close();

            Debug.Log(":" + words[0] + ":");

            if (words[0].Contains("left"))
            {
                transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y - 1, transform.rotation.eulerAngles.z);
            }
            if (words[0].Contains("right"))
            {
                transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y + 1, transform.rotation.eulerAngles.z);
            }

            if (words[1].Contains("up"))
            {
                transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y, transform.rotation.eulerAngles.z - 1);
            }
            if (words[1].Contains("down"))
            {
                transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y, transform.rotation.eulerAngles.z + 1);
            }

            /*
            if (words[2].Contains("front"))
            {
                transform.localScale = new Vector3(transform.localScale.x + 0.01f, transform.localScale.y, transform.localScale.z);
            }
            if (words[2].Contains("back"))
            {
                transform.localScale = new Vector3(transform.localScale.x - 0.01f, transform.localScale.y, transform.localScale.z);
            }*/
        }
        catch(Exception e)
        {

        }

        if (Input.GetKey(KeyCode.R))
        {
            transform.localScale = new Vector3(transform.localScale.x + 0.01f, transform.localScale.y, transform.localScale.z);
        }
        if (Input.GetKey(KeyCode.B))
        {
            transform.localScale = new Vector3(transform.localScale.x - 0.01f, transform.localScale.y, transform.localScale.z);
        }

        /*
         *  FOR TESTING ONLY
        if (Input.GetKey(KeyCode.A))
        {
            transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y - 1, transform.rotation.eulerAngles.z);
        }
        if (Input.GetKey(KeyCode.S))
        {
            transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.y + 1, transform.rotation.eulerAngles.z);
        }
        */
    }
}
