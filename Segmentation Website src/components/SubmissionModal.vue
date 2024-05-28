<template>
    <Transition name="modal">
        <div class="modal-mask">
            <div class="modal-container">

                <div class="modal-body">
                    <div class="body-container bordered">
                        <div>
                            <div role="progressbar" :aria-valuenow="totalPercentage" aria-valuemin="0"
                                aria-valuemax="100" :style="{ '--value': totalPercentage, '--size': '170px' }">
                            </div>
                            <p>Result: {{ result }}</p>
                        </div>

                        <div class="three-chart">
                            <div class="pie-box">
                                <div role="progressbar" :aria-valuenow="approvedPercentage" aria-valuemin="0"
                                    aria-valuemax="100" :style="{ '--value': approvedPercentage, '--size': '80px' }"
                                    class="approved-bar">
                                </div>
                                <p style="font-size: 14px;">Approved</p>
                            </div>
                            <div class="pie-box">
                                <div role="progressbar" :aria-valuenow="editedPercentage" aria-valuemin="0"
                                    aria-valuemax="100" :style="{ '--value': editedPercentage, '--size': '80px' }"
                                    class="edited-bar">
                                </div>
                                <p>Edited</p>
                            </div>
                            <div class="pie-box">
                                <div role="progressbar" :aria-valuenow="rejectedPercentage" aria-valuemin="0"
                                    aria-valuemax="100" :style="{ '--value': rejectedPercentage, '--size': '80px' }"
                                    class="rejected-bar">
                                </div>
                                <p>Rejected</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="toggle-radio bordered">
                            <div style="width: 150px; font-size: 16px;">
                                <p>Change Result:</p>
                            </div>
                            <div><input type="radio" name="rdo" id="yes" :checked="result != 'Rejected'"
                                    ref="approved_choice">
                                <input type="radio" name="rdo" id="no" ref="rejected_choice"
                                    :checked="result === 'Rejected'">
                                <div class="switch">
                                    <label for="yes">Approved</label>
                                    <label for="no">Rejected</label>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bordered"> <textarea v-model="additionalNotes" placeholder="Additional Notes" cols="45"
                            rows="5"></textarea>
                    </div>

                </div>

                <div class="modal-footer">
                    <div class="button-container">

                        <button class="submit-button" @click="$emit('close')">Cancel</button>
                        <button class="submit-button" id="btn" ref="btn" @click="submitClicked">
                            <p id="btnText" ref="btnText">Submit</p>
                            <div class="check-box">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
                                    <path fill="transparent" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
                                </svg>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>


<script>
export default {
    name: 'SubmissionModal',
    props: ['approvedPercentage', 'rejectedPercentage', 'editedPercentage', 'result'],
    data() {
        return {
            totalPercentage: (this.approvedPercentage + this.editedPercentage),
            additionalNotes: ''
        }
    },
    methods: {
        submitClicked() {
            this.$refs.btnText.innerHTML = "Submitted";
            this.$refs.btn.classList.add("active");

            const choice = this.$refs.approved_choice.checked ? 'Approved' : 'Rejected';
            setTimeout(() => {
                this.$emit('submit', choice, this.additionalNotes)
            }, 2000)
        },
        testFun() {

            this.$refs.approved_choice.checked = true
        }
    },
}
</script>



<style lang="scss" scoped>
.body-container {
    display: flex;
    gap: 20px;
    justify-content: center;
    align-items: center;

}

.button-container {
    position: relative;
    gap: 10px;
    display: flex;
    justify-content: right;
}

.submit-button {
    width: 85px;
    height: 30px;
    border: none;
    outline: none;
    background: #2f2f2f;
    color: #fff;
    font-size: 10px;
    border-radius: 40px;
    text-align: center;
    box-shadow: 0 6px 20px -5px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    margin: 0;

    &:hover {
        opacity: 0.8;
    }
}

.check-box {
    width: 30px;
    height: 30px;
    border-radius: 40px;
    box-shadow: 0 0 12px -2px rgba(0, 0, 0, 0.5);
    position: absolute;
    top: 0;
    right: -40px;
    opacity: 0;
}

.check-box svg {
    width: 30px;
    margin: 0px;
}

svg path {
    stroke-width: 3;
    stroke: #ffffff;
    stroke-dasharray: 34;
    stroke-dashoffset: 34;
    stroke-linecap: round;
}

.active {
    background: #ff2b75;
    transition: 1s;
}

.active .check-box {
    right: 0;
    opacity: 1;
    transition: 1s;
}

.active p {
    margin-right: 125px;
    transition: 1s;
}

.active svg path {
    stroke-dashoffset: 0;
    transition: 1s;
    transition-delay: 1s;
}

.bordered {
    //border: 1px solid black;
    padding: 5px;
    margin: 10px 0;
    border-radius: 10px;
    box-shadow: 0 0.5rem 2rem hsl(0 0% 0% / 20%);
}

.pie-box {
    display: flex;
    align-items: center;
}

.toggle-radio {
    position: relative;
    display: flex;
    //height: 50px;
    align-items: center;
}

.switch {
    position: absolute;
    right: 20px;
    width: 180px;
    height: 30px;
    text-align: center;
    background: #00bc9c;
    transition: all 0.2s ease;
    border-radius: 25px;
    font-size: 14px;
    top: 50%;
    transform: translateY(-50%);
}

.switch span {
    position: absolute;
    width: 20px;
    height: 4px;
    top: 50%;
    left: 50%;
    margin: -2px 0px 0px -4px;
    background: #fff;
    display: block;
    transform: rotate(-45deg);
    transition: all 0.2s ease;
}

.switch span:after {
    content: "";
    display: block;
    position: absolute;
    width: 4px;
    height: 12px;
    margin-top: -8px;
    background: #fff;
    transition: all 0.2s ease;
}



input[type=radio] {
    display: none;
}

.switch label {
    cursor: pointer;
    color: rgba(0, 0, 0, 0.2);
    width: 65px;
    line-height: 30px;
    transition: all 0.2s ease;
}

label[for=yes] {
    position: absolute;
    left: 10px;
    height: 20px;
}

label[for=no] {
    position: absolute;
    right: 10px;
}

#no:checked~.switch {
    background: #eb4f37;
}

#no:checked~.switch span {
    background: #fff;
    margin-left: -8px;
}

#no:checked~.switch span:after {
    background: #fff;
    height: 20px;
    margin-top: -8px;
    margin-left: 8px;
}

#yes:checked~.switch label[for=yes] {
    color: #fff;
}

#no:checked~.switch label[for=no] {
    color: #fff;
}

.three-chart {
    div {
        margin: 5px 10px;

    }
}


@keyframes progress {
    0% {
        --percentage: 0;
    }

    100% {
        --percentage: var(--value);
    }
}

@property --percentage {
    syntax: '<number>';
    inherits: true;
    initial-value: 0;
}

[role="progressbar"] {
    --percentage: var(--value);
    --primary: rgb(129, 51, 153);
    --secondary: rgba(129, 51, 153, 0.299);
    animation: progress 2s 0.5s forwards;
    width: var(--size);
    aspect-ratio: 1;
    border-radius: 50%;
    position: relative;
    overflow: hidden;
    display: grid;
    place-items: center;
}

[role="progressbar"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: conic-gradient(var(--primary) calc(var(--percentage) * 1%), var(--secondary) 0);
    mask: radial-gradient(white 55%, transparent 0);
    mask-mode: alpha;
    -webkit-mask: radial-gradient(#0000 55%, #000 0);
    -webkit-mask-mode: alpha;

}

[role="progressbar"]::after {
    counter-reset: percentage var(--value);
    content: counter(percentage) '%';
    font-family: Helvetica, Arial, sans-serif;
    font-size: calc(var(--size) / 5);
    color: var(--primary);
}


.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    transition: opacity 0.3s ease;
}

.modal-container {
    width: 400px;
    margin: auto;
    padding: 20px 20px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
}



.modal-body {
    margin: 0px 0;

    div {}
}

.modal-default-button {
    float: right;
}


.rejected-bar {
    --primary: #FF6347;
    --secondary: rgba(255, 160, 122, 0.551);
}

.edited-bar {
    --primary: #ffa600;
    --secondary: #ffa60067;
}

.approved-bar {
    --primary: #3cb372;
    --secondary: #3cb3726c;
}
</style>