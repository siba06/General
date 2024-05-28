<template>
    <div class="modal">
        <article class="modal-container">
            <header class="modal-container-header">
                <h1 class="modal-container-title">
                    How to use tool
                </h1>
                <button class="icon-button" @click="$emit('close')">
                    <i class="fa-solid fa-x"></i>
                </button>
            </header>
            <section class="modal-container-body rtf">
                <div>

                    <div class="section">
                        <h3>1. Getting Started</h3>
                        <p>Upon accessing the tool, you will find a user interface with various components tailored for
                            reviewing
                            OCT
                            images:</p>
                        <div class="sub-section">
                            <p><strong>Image and Editor Viewer:</strong> Here, you can view OCT images and annotate them
                                if
                                necessary.
                            </p>
                            <p><strong>Approval Buttons:</strong> These buttons are used to approve or reject the
                                current image.
                            </p>
                            <p><strong>Navigation Arrows:</strong> Use these arrows to navigate between different slices
                                in the
                                OCT
                                volume.</p>
                        </div>
                    </div>

                    <div class="section">
                        <h3>2. Viewing OCT Images</h3>
                        <p>Use the navigation arrows to move between slices in the OCT volume. The image and editor
                            viewer will
                            display
                            the selected OCT image, along with any existing annotations or markings.</p>
                    </div>

                    <div class="section">
                        <h3>3. Annotation and Markup</h3>
                        <p style="color: red;">Current Markup can be toggled off or on using the button in the top left
                            corner
                            of the image.</p>
                        <p>Annotations can only be added to OCT images that have been rejected. If you believe an OCT
                            image does
                            not
                            meet the required standard, click the "Reject" button. After rejecting an image, you can
                            annotate it
                            using
                            the markup tools provided in the editor viewer. Use the tools to indicate areas of concern,
                            abnormalities,
                            or other relevant information.</p>
                        <p style="color: red;">NOTE: If a gap is left between two line segments, the system will connect
                            the
                            line segments with
                            a straight line. This will appear once you have saved the changes on the markup or if you
                            click the
                            reload button on the tool panel.</p>
                    </div>

                    <div class="section">
                        <h3>4. Approving or Rejecting Images</h3>
                        <p>If you determine that an OCT image meets the required standard, click the "Approve" button.
                            Images
                            that
                            are
                            approved are considered to meet the necessary criteria for diagnosis or research purposes.
                            Rejected
                            images
                            are assumed to have been modified to an approved standard if annotations are added.</p>
                    </div>

                    <div>
                        <h3>Using the Tool Panel</h3>
                        <p>
                            The tool panel provides access to various functionalities:
                        </p>
                        <ul>
                            <li>Click on the <strong>Crop</strong> button (<i class="fa-solid fa-crop"></i>) to initiate
                                the
                                image
                                cropping mode.</li>
                            <li> The markup visibilty toggle will display an option to view/edit the current layer.</li>

                            <li>Choose the <strong>Pen</strong> tool (<i class="fa-solid fa-pen"></i>) to change the
                                current
                                layer and to draw on the image.
                            </li>
                            <li>Select the <strong>Eraser</strong> tool (<i class="fa-solid fa-eraser"></i>) to erase
                                markings,
                                this
                                will erase both original and new markings.</li>
                            <li>
                                Use the <strong>Undo</strong> button (<i class="fa-solid fa-undo"></i>) to undo the last
                                action.
                            </li>
                            <li>
                                Use the <strong>Delete</strong> button (<i class="fa-solid fa-trash"></i>) to delete all
                                existing markings.
                            </li>
                            <li>Use the <strong>Reload</strong> button (<i class="fa-solid fa-arrows-rotate"></i>) to
                                reload the
                                markup with the applied changes. This will not save the changes.</li>
                            <li>
                                The <strong>Save</strong> button (<i class="fa-solid fa-floppy-disk"></i>) will save the
                                changes
                                made. This will not overwrite the existing markup until the volume is submitted.
                            </li>
                            <li>The <strong>Cancel</strong> button (<i class="fa-solid fa-xmark"></i>) will discard any
                                unsaved
                                changes.
                            </li>
                        </ul>

                        <h3>Using the Color and Eraser Size Pickers</h3>
                        <p>
                            Below the tool panel, you'll find color and eraser size pickers:
                        </p>
                        <ul>
                            <li>If using the <strong>Pen</strong> tool, a color picker will appear allowing you to
                                select the
                                drawing
                                color. Clicking the &#x1F6C8; icon will display/hide the labels of the layer interfaces.
                            </li>
                            <li>If using the <strong>Eraser</strong> tool, an eraser size slider will appear to adjust
                                the
                                eraser
                                size.
                            </li>
                        </ul>
                    </div>
                </div>
            </section>
        </article>
    </div>
</template>


<script>
export default {
    data() {
        return {
        }
    },
    methods: {
    },
}
</script>



<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css2?family=Outfit:wght@100;200;300;400;500;600;700;800;900&display=swap");

* {
    z-index: 9999;
}

*:before,
*:after {
    box-sizing: border-box;
}

/* Some basic CSS overrides */
body {
    line-height: 1.5;
    min-height: 100vh;
    font-family: "Outfit", sans-serif;
    color: #2d232e;
    background-color: #c8c0bd;
    position: relative;
}

button,
input,
select,
textarea {
    font: inherit;
}

a {
    color: inherit;
}

/* End basic CSS override */

* {
    scrollbar-width: 0;
}

*::-webkit-scrollbar {
    background-color: transparent;
    width: 12px;
}

*::-webkit-scrollbar-thumb {
    border-radius: 99px;
    background-color: #ddd;
    border: 4px solid #fff;
}

.modal {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(#000, 0.25);
}

.modal-container {
    max-height: 90vh;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    background-color: #fff;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 15px 30px 0 rgba(#000, 0.25);

    @media (max-width: 600px) {
        width: 90%;
    }
}

.modal-container-header {
    padding: 16px 32px;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.modal-container-title {
    display: flex;
    align-items: center;
    gap: 8px;
    line-height: 1;
    font-weight: 700;
    font-size: 1.125;

    svg {
        width: 32px;
        height: 32px;
        color: #750550;
    }
}

.modal-container-body {
    padding: 24px 32px 51px;
    overflow-y: auto;
}

.rtf {

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        font-weight: 700;
    }

    h1 {
        font-size: 1.5rem;
        line-height: 1.125;
    }

    h2 {
        font-size: 1.25rem;
        line-height: 1.25;
    }

    h3 {
        font-size: 1rem;
        line-height: 1.5;
    }

    &>*+* {
        margin-top: 1em;
    }

    &>*+ :is(h1, h2, h3) {
        margin-top: 2em;
    }

    &> :is(h1, h2, h3)+* {
        margin-top: 0.75em;
    }

    ul,
    ol {
        margin-left: 20px;
        list-style-position: inside;
    }

    ol {
        list-style: numeric;
    }

    ul {
        list-style: disc;
    }
}

.modal-container-footer {
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    border-top: 1px solid #ddd;
    gap: 12px;
    position: relative;

    &:after {
        content: "";
        display: block;
        position: absolute;
        top: -51px;
        left: 24px;
        right: 24px;
        height: 50px;
        flex-shrink: 0;
        background-image: linear-gradient(to top, rgba(#fff, 0.75), transparent);
        pointer-events: none;
    }
}

.button {
    padding: 12px 20px;
    border-radius: 8px;
    background-color: transparent;
    border: 0;
    font-weight: 600;
    cursor: pointer;
    transition: 0.15s ease;

    &.is-ghost {

        &:hover,
        &:focus {
            background-color: #dfdad7;
        }
    }

    &.is-primary {
        background-color: #750550;
        color: #fff;

        &:hover,
        &:focus {
            background-color: #4a0433;
        }
    }
}

.icon-button {
    padding: 0;
    border: 0;
    background-color: transparent;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.15s ease;

    svg {
        width: 24px;
        height: 24px;
    }

    &:hover,
    &:focus {
        background-color: #dfdad7;
    }
}
</style>