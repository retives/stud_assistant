export default (await import('vue')).defineComponent({
    name: "SimpleChat",
    data() {
        return {
            messages: [
                { "role": "system", "content": "Be a helpful assistant for students, find the info on university's website and read the timetable" },
                { "role": "user", "content": "Where is the Faculty of Computer Science in the IFNTUOG" },
                { "role": "assistant", "content": "Got it! The Faculty of Computer Science of Ivano-Frankivsk National Technical University of Oil and Gas is located at Berehova Street." }
            ],
            input: "",
            apiEndpoint: "https://localhost:11434",
            apiKey: "",
            model: "qwen2.5:latest",
        };
    },
    methods: {
        // Request method to the LLM
        async sendMessage() {
            if (!this.input.trim())
                return;
            const userMsg = { role: "user", content: this.input };
            this.messages.push(userMsg);
            const inputCopy = this.input;
            this.input = "";
            try {
                const res = await fetch(this.apiEndpoint, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${this.apiKey}`,
                    },
                    body: JSON.stringify({ model: this.model, messages: this.messages }),
                });
                const data = await res.json();
                const reply = data.choices?.[0]?.message?.content || "[No response]";
                this.messages.push({ role: "assistant", content: reply });
            }
            catch (e) {
                console.error(e);
                this.messages.push({ role: "assistant", content: "Error calling API" });
            }
        },
        async formRequestJson() {
            if (!this.input.trim())
                return;
            const userMsg = { role: "user", content: this.input };
            this.messages.push(userMsg);
            const inputCopy = this.input;
            this.input = "";
        }
    },
});
const __VLS_ctx = {};
let __VLS_elements;
let __VLS_components;
let __VLS_directives;
/** @type {__VLS_StyleScopedClasses['messages']} */ ;
/** @type {__VLS_StyleScopedClasses['messages']} */ ;
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
// CSS variable injection 
// CSS variable injection end 
__VLS_asFunctionalElement(__VLS_elements.div, __VLS_elements.div)({
    ...{ class: "chat-app" },
});
__VLS_asFunctionalElement(__VLS_elements.div, __VLS_elements.div)({
    ...{ class: "messages" },
});
for (const [msg, i] of __VLS_getVForSourceType((__VLS_ctx.messages))) {
    // @ts-ignore
    [messages,];
    __VLS_asFunctionalElement(__VLS_elements.div, __VLS_elements.div)({
        key: (i),
        ...{ class: (msg.role) },
    });
    __VLS_asFunctionalElement(__VLS_elements.b, __VLS_elements.b)({});
    (msg.role);
    (msg.content);
}
__VLS_asFunctionalElement(__VLS_elements.div, __VLS_elements.div)({
    ...{ class: "composer" },
});
__VLS_asFunctionalElement(__VLS_elements.input)({
    ...{ onKeyup: (__VLS_ctx.formRequestJson) },
    placeholder: "Type a message...",
});
(__VLS_ctx.input);
// @ts-ignore
[formRequestJson, input,];
__VLS_asFunctionalElement(__VLS_elements.button, __VLS_elements.button)({
    ...{ onClick: (__VLS_ctx.formRequestJson) },
});
// @ts-ignore
[formRequestJson,];
/** @type {__VLS_StyleScopedClasses['chat-app']} */ ;
/** @type {__VLS_StyleScopedClasses['messages']} */ ;
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
var __VLS_dollars;
let __VLS_self;
//# sourceMappingURL=App.vue.js.map