using UnityEngine;


// This script helps set up individual organ interactables
public class OrganInteractableSetup : MonoBehaviour
{
    [Tooltip("The main digestive system model")]
    public GameObject digestiveSystemModel;
    
    [Tooltip("The organ manager script")]
    public OrganInfoManager organManager;
    
    [System.Serializable]
    public class OrganSetup
    {
        public string organName;
        public Vector3 position;
        public Vector3 size;
        public ColliderType colliderType;
    }
    
    public enum ColliderType
    {
        Box,
        Sphere,
        Capsule
    }
    
    public OrganSetup[] organSetups;
    
    [ContextMenu("Setup Organ Interactables")]
    public void SetupOrganInteractables()
    {
        if (digestiveSystemModel == null)
        {
            Debug.LogError("Digestive system model not assigned!");
            return;
        }
        
        foreach (OrganSetup setup in organSetups)
        {
            // Create organ interactable
            GameObject organObj = new GameObject(setup.organName + "Collider");
            organObj.transform.parent = digestiveSystemModel.transform;
            organObj.transform.localPosition = setup.position;
            
            // Add appropriate collider
            switch (setup.colliderType)
            {
                case ColliderType.Box:
                    BoxCollider boxCollider = organObj.AddComponent<BoxCollider>();
                    boxCollider.size = setup.size;
                    boxCollider.isTrigger = true;
                    break;
                    
                case ColliderType.Sphere:
                    SphereCollider sphereCollider = organObj.AddComponent<SphereCollider>();
                    sphereCollider.radius = setup.size.x / 2; // Use x as diameter
                    sphereCollider.isTrigger = true;
                    break;
                    
                case ColliderType.Capsule:
                    CapsuleCollider capsuleCollider = organObj.AddComponent<CapsuleCollider>();
                    capsuleCollider.radius = setup.size.x / 2;
                    capsuleCollider.height = setup.size.y;
                    capsuleCollider.isTrigger = true;
                    break;
            }
            
            // Add XR Simple Interactable instead of XR Grab Interactable
            UnityEngine.XR.Interaction.Toolkit.Interactables.XRSimpleInteractable interactable = organObj.AddComponent<UnityEngine.XR.Interaction.Toolkit.Interactables.XRSimpleInteractable>();
            
            // Add the click detector
            OrganClickDetector clickDetector = organObj.AddComponent<OrganClickDetector>();
            clickDetector.infoManager = organManager;
            
            Debug.Log("Created interactable for: " + setup.organName);
        }
    }
}