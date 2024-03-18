import { configureStore } from '@reduxjs/toolkit';
import {thunk} from 'redux-thunk';
import { combineReducers } from 'redux';
import { bookListReducer } from './reducers/bookReducers';
import { userRegisterReducer } from './reducers/registerReducers';
import { userLoginReducer } from './reducers/userReducers';
import { genreListReducer } from './reducers/genreReducers';
import { interactionListReducer, interactionDetailsReducer, interactionListByBookReducer} from './reducers/interactionReducers'; 
import { authorListReducer, authorDetailsReducer, authorCreateReducer} from './reducers/authorReducers';
import { feedbackReducer, feedbackListReducer } from './reducers/feedbackReducers';
import { bookDetailsReducer } from './reducers/bookReducers';
import searchReducer from './reducers/searchReducers';
import { otpReducer } from './reducers/otpReducers';

const reducer = combineReducers({
    bookList: bookListReducer,
    userRegister: userRegisterReducer,
    userLogin: userLoginReducer,
    genreList: genreListReducer,
    interactionListByBook: interactionListByBookReducer,
    interactionList: interactionListReducer,
    interactionDetails: interactionDetailsReducer, 
    feedback: feedbackReducer,
    bookDetails: bookDetailsReducer,
    search: searchReducer,
    otp: otpReducer, 
    feedbackList: feedbackListReducer,
    authorList: authorListReducer,
    authorDetails: authorDetailsReducer,
    authorCreate: authorCreateReducer,


});

const userInfoFromStorage = localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : null;

const initialState = {
    userLogin: { userInfo: userInfoFromStorage },
    userRegister: {userInfo: userInfoFromStorage},
};

const store = configureStore({
    reducer,
    preloadedState: initialState,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(thunk),
});

export default store;
