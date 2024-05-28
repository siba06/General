<template>
    <div>
        <nav class="slidemenu">


            <!-- Item 1 -->
            <input type="radio" name="slideItem" id="slide-item-1" class="slide-toggle" value="introduction"
                v-model="chosenTab" checked />
            <label for="slide-item-1"><span>Introduction</span></label>

            <!-- Item 2 -->
            <input type="radio" name="slideItem" id="slide-item-2" class="slide-toggle" value="selecting"
                v-model="chosenTab" />
            <label for="slide-item-2"><span>Selecting Sample Size</span></label>


            <!-- Item 3 -->
            <input type="radio" name="slideItem" id="slide-item-3" class="slide-toggle" value="editing"
                v-model="chosenTab" />
            <label for="slide-item-3"><span>Editing and Approving Sample</span></label>

            <!-- Item 4 -->
            <input type="radio" name="slideItem" id="slide-item-4" class="slide-toggle" value="submitting"
                v-model="chosenTab" />
            <label for="slide-item-4"><span>Submitting Sample Review</span></label>

            <!-- Item 5 -->
            <input type="radio" name="slideItem" id="slide-item-5" class="slide-toggle" value="additional"
                v-model="chosenTab" />
            <label for="slide-item-5"><span>Additional Information</span></label>

            <div class="clear"></div>

            <!-- Bar -->
            <div class="slider">
                <div class="bar"></div>
            </div>
        </nav>
    </div>
    <div class="tab-content">
        <h2>{{ tabs[chosenTab] }}</h2>

        <div v-if="chosenTab === 'introduction'">
            <div>
                <p>This is a web-based tool designed for viewing, editing, and approving segmentations of Optical
                    Coherence
                    Tomography (OCT) images. It provides dedicated interfaces for editing specific retinal layers,
                    including:
                </p>
                <br>
                <ul>
                    <li>Inner Limiting Membrane (ILM)</li>
                    <li>RNFL - GCL interface</li>
                    <li>GCL - IPL interface</li>
                    <li>IPL - INL interface</li>
                    <li>INL - OPL interface</li>
                    <li>OPL - ONL interface</li>
                    <li>External Limiting Membrane (ELM)</li>
                    <li>Inner boundary of EZ</li>
                    <li>Inner boundary of RPE/IZ complex</li>
                    <li>Bruch's Membrane</li>
                    <li>Choroid - sclera interface</li>
                </ul>
            </div>
            <div>
                <p>In the Pending tab, accessible from the menu in the top-left corner, patients with volumes awaiting
                    approval
                    are listed by their unique patient IDs. Upon selecting a patient, a list of volumes obtained for
                    that
                    patient is displayed. These volumes are color-coded based on their completion status, which can be:
                </p>
                <br>
                <ul class="pending-list">
                    <li class="pending-item unchecked"><span class="circle"
                            style="background-color: #dcdcdc;"></span>Unchecked:
                        Volumes that have not yet been reviewed.</li>
                    <li class="pending-item approved"><span class="circle"
                            style="background-color: #8effa4;"></span>Approved:
                        Volumes that have been reviewed and approved without any modifications.</li>
                    <li class="pending-item rejected"><span class="circle"
                            style="background-color: #ffb8b8;"></span>Rejected:
                        Volumes that have been reviewed and rejected due to issues or inaccuracies.</li>
                    <li class="pending-item modified"><span class="circle"
                            style="background-color: #fffa8e;"></span>Approved
                        with Modifications: Volumes that have been reviewed and approved with some modifications or
                        annotations.</li>
                </ul>
            </div>
        </div>

        <div v-if="chosenTab === 'selecting'">
            <div>
                <p>
                    On selection of a volume to review, the sample proportion, minimum, and maximum number of slices can
                    be
                    specified. This feature is designed to aid in selecting a representative subset of data for analysis
                    or
                    visualization.
                </p>
                <br>
                <h3>Setting Sample Proportion:</h3>
                <ol>
                    <li>Navigate to the Pending tab and select the volume to be reviewed. This will prompt a pop-up.
                    </li>
                    <li>Use the slider or input field labeled "Sample Proportion" to specify the percentage of volume to
                        sample.
                    </li>
                    <li>The slider allows you to visually adjust the percentage between 10% and 50%.</li>
                    <li>You can also manually input the desired percentage in the input field provided.</li>
                    <li>Ideally, the sample proportion should be between 20% and 40% for optimal representation.</li>
                </ol>
                <br>
                <h3>Optional: Setting Minimum and Maximum Slices:</h3>
                <ul>
                    <li>Optionally, specify the minimum and maximum number of slices for the sample.</li>
                    <li>Input the desired values in the respective fields labeled "Minimum number of slices" and
                        "Maximum number of slices".</li>
                    <li>These values help ensure that the sample size meets specific criteria, such as ensuring an
                        adequate representation of data.</li>
                </ul>

                <br>
                <h3>Tooltip Information:</h3>
                <ul>
                    <li>Hover over the ℹ️ icon next to each input field to view additional information and guidelines
                        related to that input.</li>
                    <li>Tooltips provide helpful hints for making informed selections, such as best practices and
                        recommendations.</li>
                </ul>

                <br>
                <h3>Confirm or Cancel Selection:</h3>
                <ul>
                    <li>Once you've specified the sample proportion and optional minimum/maximum slices, click the
                        "Confirm" button to proceed.</li>
                    <li>If you wish to cancel the selection process, click the "Cancel" button.</li>
                </ul>
            </div>
        </div>
        <div v-if="chosenTab === 'editing'">
            <div class="section">
                <h3>1. Getting Started</h3>
                <p>Upon accessing the tool, you will find a user interface with various components tailored for
                    reviewing
                    OCT
                    images:</p>
                <div class="sub-section">
                    <p><strong>Image and Editor Viewer:</strong> Here, you can view OCT images and annotate them if
                        necessary.
                    </p>
                    <p><strong>Approval Buttons:</strong> These buttons are used to approve or reject the current image.
                    </p>
                    <p><strong>Navigation Arrows:</strong> Use these arrows to navigate between different slices in the
                        OCT
                        volume.</p>
                </div>
            </div>

            <div class="section">
                <h3>2. Viewing OCT Images</h3>
                <p>Use the navigation arrows to move between slices in the OCT volume. The image and editor viewer will
                    display
                    the selected OCT image, along with any existing annotations or markings.</p>
            </div>

            <div class="section">
                <h3>3. Annotation and Markup</h3>
                <p style="color: red;">Current Markup can be toggled off or on using the button in the top left corner
                    of the image.</p>
                <p>Annotations can only be added to OCT images that have been rejected. If you believe an OCT image does
                    not
                    meet the required standard, click the "Reject" button. After rejecting an image, you can annotate it
                    using
                    the markup tools provided in the editor viewer. Use the tools to indicate areas of concern,
                    abnormalities,
                    or other relevant information.</p>
                <p style="color: red;">NOTE: If a gap is left between two line segments, the system will connect the
                    line segments with
                    a straight line. This will appear once you have saved the changes on the markup or if you click the
                    reload button on the tool panel.</p>
            </div>

            <div class="section">
                <h3>4. Approving or Rejecting Images</h3>
                <p>If you determine that an OCT image meets the required standard, click the "Approve" button. Images
                    that
                    are
                    approved are considered to meet the necessary criteria for diagnosis or research purposes. Rejected
                    images
                    are assumed to have been modified to an approved standard if annotations are added.</p>
            </div>

            <div>
                <h3>Using the Tool Panel</h3>
                <p>
                    The tool panel provides access to various functionalities:
                </p>
                <ul>
                    <li>Click on the <strong>Crop</strong> button (<i class="fa-solid fa-crop"></i>) to initiate the
                        image
                        cropping mode.</li>
                    <li> The markup visibilty toggle will display an option to view/edit the current layer.</li>

                    <li>Choose the <strong>Pen</strong> tool (<i class="fa-solid fa-pen"></i>) to change the current
                        layer and to draw on the image.
                    </li>
                    <li>Select the <strong>Eraser</strong> tool (<i class="fa-solid fa-eraser"></i>) to erase markings,
                        this
                        will erase both original and new markings.</li>
                    <li>
                        Use the <strong>Undo</strong> button (<i class="fa-solid fa-undo"></i>) to undo the last action.
                    </li>
                    <li>
                        Use the <strong>Delete</strong> button (<i class="fa-solid fa-trash"></i>) to delete all
                        existing markings.
                    </li>
                    <li>Use the <strong>Reload</strong> button (<i class="fa-solid fa-arrows-rotate"></i>) to reload the
                        markup with the applied changes. This will not save the changes.</li>
                    <li>
                        The <strong>Save</strong> button (<i class="fa-solid fa-floppy-disk"></i>) will save the changes
                        made. This will not overwrite the existing markup until the volume is submitted.
                    </li>
                    <li>The <strong>Cancel</strong> button (<i class="fa-solid fa-xmark"></i>) will discard any unsaved
                        changes.
                    </li>
                </ul>

                <h3>Using the Color and Eraser Size Pickers</h3>
                <p>
                    Below the tool panel, you'll find color and eraser size pickers:
                </p>
                <ul>
                    <li>If using the <strong>Pen</strong> tool, a color picker will appear allowing you to select the
                        drawing
                        color. Clicking the &#x1F6C8; icon will display/hide the labels of the layer interfaces.</li>
                    <li>If using the <strong>Eraser</strong> tool, an eraser size slider will appear to adjust the
                        eraser
                        size.
                    </li>
                </ul>
            </div>
        </div>

        <div v-if="chosenTab === 'submitting'">
            <div>
                <p>Upon reviewing all slices, a submit button will become available. Clicking submit will display the
                    results of the submission.</p>

                <p>After reviewing the information, you can select a different final outcome if you believe the
                    determined
                    result to be incorrect. Optionally, any additonal notes can be left in this section.</p>

            </div>
        </div>

        <div v-if="chosenTab === 'additional'">
            <div>
                <p>For any additional information or queries, please contact:</p>
                <ul>
                    <li>Siba Al Dalaty:
                        <ul>
                            <li>Email:
                                <a href="mailto:siba.al-dalaty@durham.ac.uk">
                                    siba.al-dalaty@durham.ac.uk
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>

            </div>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return {
            chosenTab: 'introduction',
            tabs: {
                introduction: 'Introduction',
                selecting: 'Selecting Sample Size',
                editing: 'Editing and Approval',
                submitting: 'Submitting Approvals',
                additional: 'Contact Information'
            }
        }
    },
    created() {
        document.title = "About";
    },
}
</script>

<style scoped>
div {
    text-align: left;
}

ul {
    list-style-position: inside;
}

ol {
    list-style-position: inside;

}

.pending-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.pending-item {
    display: flex;
    border-radius: 10px;
    align-items: center;
    margin: 5px;
}

.unchecked {
    background-color: #dcdcdc;
    color: #333;
}

.approved {
    background-color: #8effa4;
    color: #333;
}

.rejected {
    background-color: #ffb8b8;
    color: #333;
}

.modified {
    background-color: #fffa8e;
    color: #333;
}

.circle {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 10px;
}

.clear {
    clear: both;
}


.slide-toggle {
    display: none;
}

.slidemenu {
    font-family: arial, sans-serif;
    max-width: 80%;
    margin: 50px auto;
    overflow: hidden;
}

.slidemenu label {
    width: 20%;
    text-align: center;
    display: block;
    float: left;
    color: #333;
    opacity: 0.2;

}

.slidemenu label:hover {
    cursor: pointer;
    color: #666;
}

.slidemenu label span {
    display: block;
    padding: 10px;
}

.slidemenu label .icon {
    font-size: 20px;
    border: solid 2px #333;
    text-align: center;
    height: 50px;
    width: 50px;
    display: block;
    margin: 0 auto;
    line-height: 50px;
    border-radius: 50%;
}

/*Bar Style*/

.slider {
    width: 100%;
    height: 5px;
    display: block;
    background: #ccc;
    margin-top: 10px;
    border-radius: 5px;
}

.slider .bar {
    width: 20%;
    height: 5px;
    background: #333;
    border-radius: 5px;
}


/*Animations*/
.slidemenu label,
.slider .bar {
    transition: all 500ms ease-in-out;
    -webkit-transition: all 500ms ease-in-out;
    -moz-transition: all 500ms ease-in-out;
}

/*Toggle*/

.slidemenu .slide-toggle:checked+label {
    opacity: 1;
}



.slidemenu #slide-item-1:checked~.slider .bar {
    margin-left: 0;
}

.slidemenu #slide-item-2:checked~.slider .bar {
    margin-left: 20%;
}

.slidemenu #slide-item-3:checked~.slider .bar {
    margin-left: 40%;
}

.slidemenu #slide-item-4:checked~.slider .bar {
    margin-left: 60%;
}

.slidemenu #slide-item-5:checked~.slider .bar {
    margin-left: 80%;
}

.tab-content {
    padding: 20px;
    border: 1px solid #ccc;
    margin-top: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.tab-content div {
    margin: 20px;
}
</style>