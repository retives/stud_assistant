declare const _default: import("vue").DefineComponent<{}, {}, {
    messages: {
        role: string;
        content: string;
    }[];
    input: string;
    apiEndpoint: string;
    apiKey: string;
    model: string;
}, {}, {
    sendMessage(): Promise<void>;
    formRequestJson(): Promise<void>;
}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<{}> & Readonly<{}>, {}, {}, {}, {}, string, import("vue").ComponentProvideOptions, true, {}, any>;
export default _default;
