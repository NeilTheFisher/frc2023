from threading import Thread

from ntcore import Event, NetworkTableInstance, EventFlags
import wpilib

from constants.ArmConstants import ArmConstants


# ! not currently used
def configureArmAnglePreferences():
    nt = NetworkTableInstance.getDefault()
    listeners = []

    preferences = nt.getTable("Preferences")

    # wpilib.SmartDashboard.getBoolean("Save Arm Angles", False)

    for gamePiece in ArmConstants.angles:
        for angleType in ArmConstants.angles[gamePiece]:
            for subsystemType in ArmConstants.angles[gamePiece][angleType]:
                entryName = f"{gamePiece}/{angleType}/{subsystemType}"
                wpilib.Preferences.setDouble(
                    entryName,
                    ArmConstants.angles[gamePiece][angleType][subsystemType],
                )

                def setAngle(
                    evt: Event,
                    entryName=entryName,
                    gamePiece=gamePiece,
                    angleType=angleType,
                    subsystemType=subsystemType,
                ) -> None:
                    if hasattr(evt.data, "value"):
                        newValue = evt.data.value.getDouble()
                        print(f"Setting {entryName} to {newValue}")
                        ArmConstants.angles[gamePiece][angleType][
                            subsystemType
                        ] = newValue

                listeners.append(
                    nt.addListener(
                        preferences.getEntry(entryName),
                        EventFlags.kValueRemote,
                        setAngle,
                    )
                )

    # for saving to json
    # TODO not necessary right now sense it is never used/deserialized
    smartDashboard = nt.getTable("SmartDashboard")
    saveArmAnglesEntry = smartDashboard.getEntry("Save Arm Angles")
    saveArmAnglesEntry.setBoolean(False)

    def saveArmAngles(evt: Event):
        if not hasattr(evt.data, "value") or evt.data.value.getBoolean() == False:
            return

        def doSave():
            import json

            fileName = "arm_angles.json"
            print(f"Saving arm angles to {fileName}")
            with open(fileName, "w") as f:
                jsonAngles = {}
                for gamePiece in ArmConstants.angles:
                    jsonAngles[gamePiece.name] = {}
                    for angleType in ArmConstants.angles[gamePiece]:
                        jsonAngles[gamePiece.name][angleType.name] = {}
                        for subsystemType in ArmConstants.angles[gamePiece][angleType]:
                            jsonAngles[gamePiece.name][angleType.name][
                                subsystemType.name
                            ] = ArmConstants.angles[gamePiece][angleType][subsystemType]
                json.dump(jsonAngles, f, indent=2)

            saveArmAnglesEntry.setBoolean(False)

        Thread(target=doSave).start()

    listeners.append(
        nt.addListener(
            saveArmAnglesEntry,
            EventFlags.kValueRemote,
            saveArmAngles,
        )
    )

    def removeListeners() -> None:
        for listener in listeners:
            nt.removeListener(listener)

    return removeListeners
