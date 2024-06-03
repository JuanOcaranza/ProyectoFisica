'use client';

import SubmitButton from "@/components/forms/submit-button";
import { createVideo } from "@/lib/actions";
import { useFormState } from "react-dom";
import TextFormField from "@/components/forms/text-form-field";

const initialState = {
    message: "",
}

export default function CreateVideoForm() {
    const [state, formAction] = useFormState(createVideo, initialState);

    return (
        <form action={formAction}>
            <TextFormField name="name" label="Name" required />
            <TextFormField name="extension" label="Extension" required />
            <TextFormField name="distance_elbow_wrist" label="Distance from Elbow to Wrist (m)" required />
            <TextFormField name="mass_weight" label="Mass of Weight (kg)" required />
            <TextFormField name="mass_forearm" label="Mass of Forearm (kg)" required />
            <TextFormField name="radius_bicep" label="Radius of Bicep (m)" required />
            <TextFormField name="height_shoulder" label="Height of Shoulder (m)" required />
            <SubmitButton>Submit</SubmitButton>
            <p aria-live="polite" className="sr-only">
                {state?.message}
            </p>
        </form>
    )
}