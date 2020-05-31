using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using UnityEngine.Windows.Speech;

public class DictationScript : MonoBehaviour
{
    [SerializeField]
    private Text m_Hypotheses;

    [SerializeField]
    private Text m_Recognitions;

    bool tiger;
    bool tiger2;
    bool car;
    bool soccer;
    bool skateboard;

    public GameObject tigerObject;
    public GameObject tigerObject2;
    public GameObject tigerObject3;
    public GameObject soccerBall;
    public GameObject skateboardObject;

    private DictationRecognizer m_DictationRecognizer;

    void Start()
    {
        tiger = false;
        tiger2 = false;
        car = false;
        soccer = false;
        skateboard = false;
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        {

            Debug.LogFormat("Dictation result: {0}", text);
            m_Recognitions.text += text + "\n";
            if (text.Contains("end"))
            {
                Debug.Log("ENDING");
                SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
        };

        m_DictationRecognizer.DictationHypothesis += (text) =>
        {
            if (text.Contains("create a tiger") && !tiger)
            {
                tiger = true;
                Debug.Log("CREATING TIGER");
                createTiger();
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("create 2 tigers") && !tiger2)
            {
                tiger2 = true;
                Debug.Log("CREATING 2 TIGERS");
                createTiger2();
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("create a soccer") && !soccer)
            {
                soccer = true;
                Debug.Log("CREATING SOCCER BALL");
                createBall();
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("on skateboard"))
            {
                Debug.Log("GETTING ON SKATEBOARD");
                transform.position = new Vector3(17.78f, transform.position.y, 25.52f);
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("off skateboard"))
            {
                Debug.Log("GETTING OFF SKATEBOARD");
                transform.position = new Vector3(18.78f, transform.position.y, 25.52f);
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("create a skateboard") && !skateboard)
            {
                skateboard = true;
                Debug.Log("CREATING SKATEBOARD");
                createSkateboard();
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            else if (text.Contains("go to school"))
            {
                Debug.Log("CREATING SKATEBOARD");
                SceneManager.LoadScene("New Scene 1");
                //SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            }
            Debug.LogFormat("Dictation hypothesis: {0}", text);
            m_Hypotheses.text += text;
        };

        m_DictationRecognizer.DictationComplete += (completionCause) =>
        {
            if (completionCause != DictationCompletionCause.Complete)
                Debug.LogErrorFormat("Dictation completed unsuccessfully: {0}.", completionCause);
        };

        m_DictationRecognizer.DictationError += (error, hresult) =>
        {
            Debug.LogErrorFormat("Dictation error: {0}; HResult = {1}.", error, hresult);
        };

        m_DictationRecognizer.Start();
    }

    public void Update()
    {
        if (Input.GetMouseButtonDown(1))
        {
            kickBall();
        }
    }

    public void createTiger()
    {
        tigerObject.SetActive(true);
    }
    
    public void createTiger2()
    {
        tigerObject2.SetActive(true);
        tigerObject3.SetActive(true);
    }

    public void createCar() {

    }

    public void createBall()
    {
        soccerBall.SetActive(true);        
    }

    public void kickBall()
    {
        soccerBall.GetComponent<Rigidbody>().velocity = new Vector3(10, 3, soccerBall.GetComponent<Rigidbody>().velocity.z);
    }

    public void createSkateboard()
    {
        skateboardObject.SetActive(true);
    }
}