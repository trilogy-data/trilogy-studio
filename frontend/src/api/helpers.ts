import axios from 'axios';

const axiosHelpers = {
    getErrorMessage(error: Error) {
        let base = 'An error occured.'
        if (axios.isAxiosError(error)) {
            base = error.message;
            if (error.response && error.response.data) {
                base = error.response.data;
            }
        }
        return base;
    }
};


export default axiosHelpers;