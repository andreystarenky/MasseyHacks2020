using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerControls : MonoBehaviour
{
    public float height = 1.6f;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 moveDirection = new Vector3(Input.GetAxis("Horizontal"), 2, Input.GetAxis("Vertical"));
        //moveDirection = Camera.main.transform.TransformDirection(moveDirection);
        //transform.localEulerAngles = new Vector3(Camera.main.transform.localEulerAngles.x, transform.localEulerAngles.y, Camera.main.transform.localEulerAngles.z);

        //GameObject ChildGameObject1 = this.gameObject.transform.GetChild(0).gameObject;

        //Debug.Log(Camera.main.gameObject.GetAxis("Horizontal"));
        if (Input.GetMouseButton(0)){
            //transform.Translate(Vector3.forward * 3 * Time.deltaTime);
            transform.position = transform.position + Camera.main.transform.forward * 3   * Time.deltaTime;
            transform.position = new Vector3(transform.position.x, height, transform.position.z);
        }
    }
}
