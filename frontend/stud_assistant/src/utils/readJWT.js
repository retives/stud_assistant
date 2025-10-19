import {jwtDecode} from "jwt-decode";

export function readJWT(token) {
    try {
        const decoded = jwtDecode(token);
        console.log("Decoded JWT:", decoded);
        return decoded;
    }catch (error) {
        console.error("Invalid JWT token:", error);
        return null;
    }
}
