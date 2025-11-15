import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function BetsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>My Bets Screen (To be implemented)</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    color: '#fff',
    fontSize: 18,
  },
});
