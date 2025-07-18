using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class bubble_column : UdonSharpBehaviour
{
    // Acceleration and termina velocity for riding bubble column elevators
    const float BUBBLE_ACCELERATION = 25f; // m/s²
    const float BUBBLE_VELOCITY = 11f; // m/s
    
    private long previous_ticks = 0;
    
    public override void OnPlayerTriggerEnter(VRCPlayerApi player)
    {
        previous_ticks = 0;
    }
    
    public override void OnPlayerTriggerExit(VRCPlayerApi player)
    {
        previous_ticks = 0;
    }
    
    public override void OnPlayerTriggerStay(VRCPlayerApi player)
    {
        if (!player.isLocal) return;

        Vector3 v = player.GetVelocity();

        long current_ticks = System.DateTime.UtcNow.Ticks; // Units of 0.1 us
        //long ticks = current_ticks - previous_ticks;
        //float seconds = ticks/10000000f;
        float Δt = (current_ticks - previous_ticks) / 10000000f; // s
        previous_ticks = current_ticks;

        // At 1 s, this can trigger a hard bounce if the player pops out of the
        // elevator for slightly less than 1 s. At 0.01 s, the elevator doesn't
        // work at all because the framerate isn't high enough.
        if (Δt > 1) return;

        // Terminal velocity should target 11 m/s, per Minecraft Wiki
        // TODO I need to account for drag from world velocity for getting to
        // 11 m/s terminal velocity
        //float g = -Physics.gravity.y;
        //float damping = 1f - v.y/11f*20f/(20f + g); // Fluid damping
        //v.y += 20f*Δt*damping; // Constant acceleration

        // g is theoretically variable here, so recalculate damping constant
        // before use
        float damping = (BUBBLE_ACCELERATION + Physics.gravity.y) /
            BUBBLE_VELOCITY;
        v.y -= Δt * damping * v.y;
        v.y += Δt * BUBBLE_ACCELERATION;
        player.SetVelocity(v);
    }
}
