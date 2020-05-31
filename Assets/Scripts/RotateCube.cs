using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class RotateCube : MonoBehaviour
{
    public float spinForce;
    private bool spinning;

    // Start is called before the first frame update
    void Start()
    {
        gameObject.GetComponent<Rigidbody>().useGravity = false;
        spinning = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (spinning)
        {
            transform.Rotate(0, spinForce * Time.deltaTime, 0);
        }
        else
        {
            transform.Rotate(spinForce * Time.deltaTime * 3, spinForce * Time.deltaTime * 3, spinForce * Time.deltaTime * 3);
        }
        //Debug.Log("RUNTIME");
    }

    public void changeSpin()
    {
        spinning = false;
        gameObject.GetComponent<Rigidbody>().velocity = new Vector3(gameObject.GetComponent<Rigidbody>().velocity.x, 5, gameObject.GetComponent<Rigidbody>().velocity.z);
        Debug.Log("POINTING");
        //spinForce = 1000;
        gameObject.GetComponent<Rigidbody>().useGravity = true;

        gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 200, 200);
    }
}
