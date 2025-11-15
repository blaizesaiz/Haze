import React from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import api from '../services/api';

export default function HomeScreen({ navigation }: any) {
  const { data: sports, isLoading } = useQuery({
    queryKey: ['sports'],
    queryFn: async () => {
      const response = await api.get('/sports');
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <View style={styles.container}>
        <Text style={styles.loadingText}>Loading sports...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to Haze</Text>
      <Text style={styles.subtitle}>Choose a sport to start betting</Text>

      <FlatList
        data={sports}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.sportCard}
            onPress={() => navigation.navigate('Events', { sportKey: item.key })}
          >
            <View style={styles.sportIcon}>
              <Ionicons name="trophy" size={32} color="#0ea5e9" />
            </View>
            <View style={styles.sportInfo}>
              <Text style={styles.sportName}>{item.name}</Text>
              <Text style={styles.sportSubtext}>View events</Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#94a3b8" />
          </TouchableOpacity>
        )}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    padding: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginTop: 8,
    marginBottom: 24,
  },
  loadingText: {
    color: '#94a3b8',
    textAlign: 'center',
    marginTop: 100,
  },
  listContainer: {
    paddingBottom: 20,
  },
  sportCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  sportIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(14, 165, 233, 0.1)',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  sportInfo: {
    flex: 1,
  },
  sportName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  sportSubtext: {
    fontSize: 14,
    color: '#94a3b8',
    marginTop: 4,
  },
});
